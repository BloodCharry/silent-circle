import os
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from sqlalchemy.pool import NullPool
from dotenv import load_dotenv

load_dotenv(".env.test")

from app.core import config  # type: ignore
from app.models.base import Base  # type: ignore
from app.db.session import get_session, init_engine  # type: ignore


@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database():
    db_url = os.environ.get("DATABASE_URL") or config.settings.DATABASE_URL
    engine = create_async_engine(db_url, echo=False, future=True, poolclass=NullPool)
    init_engine(db_url)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def db_session():
    """Создаёт отдельную сессию и очищает все таблицы после каждого теста."""
    db_url = os.environ.get("DATABASE_URL") or config.settings.DATABASE_URL
    engine = create_async_engine(db_url, echo=False, future=True, poolclass=NullPool)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        yield session

    # очищаем таблицы в отдельном connection
    async with engine.begin() as conn:
        await conn.execute(text("""
            DO $$
            DECLARE
                tab RECORD;
            BEGIN
                FOR tab IN
                    SELECT tablename FROM pg_tables WHERE schemaname = 'public'
                LOOP
                    EXECUTE 'TRUNCATE TABLE ' || quote_ident(tab.tablename) || ' RESTART IDENTITY CASCADE;';
                END LOOP;
            END $$;
        """))

    await engine.dispose()


@pytest_asyncio.fixture
async def client(db_session):
    from app.main import app  # type: ignore

    async def override_get_session():
        async with db_session.bind.connect() as conn:
            async with AsyncSession(bind=conn, expire_on_commit=False) as session:
                yield session

    app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()
