# app/db/session.py
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.core.config import settings  # type: ignore

_engine = None
_AsyncSessionLocal = None


def init_engine(url: str | None = None):
    global _engine, _AsyncSessionLocal
    url = url or settings.DATABASE_URL
    assert url.startswith("postgresql+asyncpg://"), f"Expected asyncpg URL, got {url}"
    _engine = create_async_engine(url, echo=False, future=True)
    _AsyncSessionLocal = async_sessionmaker(
        bind=_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


def get_engine():
    return _engine


def get_sessionmaker():
    return _AsyncSessionLocal


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    if _AsyncSessionLocal is None:
        raise RuntimeError("Database engine is not initialized. Call init_engine() first.")
    async with _AsyncSessionLocal() as session:
        yield session
