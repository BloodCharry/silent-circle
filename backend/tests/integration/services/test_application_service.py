import pytest
import secrets
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.application_service import ApplicationService
from app.schemas.application import ApplicationCreate
from app.models.application import Application
from app.models.user import User


@pytest.mark.asyncio
class TestApplicationService:
    async def _create_user(self, db_session: AsyncSession, idx: int = 0) -> User:
        user = User(
            telegram_id=secrets.randbelow(2_147_483_647),
            first_name=f"App{idx}",
            last_name="Tester",
            status="student",
            role="user",
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        return user

    async def test_create_application(self, db_session: AsyncSession) -> None:
        user = await self._create_user(db_session)
        app_in = ApplicationCreate(user_id=user.id)
        application: Application = await ApplicationService.create_application(db_session, app_in)
        assert isinstance(application, Application)
        assert application.user_id == user.id
        assert application.status == "pending"
        assert application.review_comment is None

    async def test_get_application_not_found(self, db_session: AsyncSession) -> None:
        with pytest.raises(Exception) as exc:
            await ApplicationService.get_application(db_session, "00000000-0000-0000-0000-000000000000")
        assert "Application not found" in str(exc.value)

    async def test_list_applications(self, db_session: AsyncSession) -> None:
        for i in range(2):
            user = await self._create_user(db_session, idx=i)
            app_in = ApplicationCreate(user_id=user.id)
            await ApplicationService.create_application(db_session, app_in)

        result = await ApplicationService.list_applications(db_session)
        assert len(result) == 2
        assert all(isinstance(a, Application) for a in result)
        assert all(a.review_comment is None for a in result)
