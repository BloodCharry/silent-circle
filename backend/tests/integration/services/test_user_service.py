import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.services.user_service import UserService
from app.schemas.user import UserCreate
from app.models.user import User


@pytest.mark.asyncio
async def test_create_user(db_session: AsyncSession) -> None:
    user_in = UserCreate(
        telegram_id=123456,
        first_name="Test",
        last_name="User",
        status="student",
        role="user"
    )
    user: User = await UserService.create_user(db_session, user_in)
    assert isinstance(user, User)
    assert user.telegram_id == 123456
    assert user.first_name == "Test"


@pytest.mark.asyncio
async def test_get_user_success(db_session: AsyncSession) -> None:
    user_in = UserCreate(
        telegram_id=654321,
        first_name="Another",
        last_name="User",
        status="student",
        role="user"
    )
    created = await UserService.create_user(db_session, user_in)
    fetched = await UserService.get_user(db_session, str(created.id))
    assert fetched.id == created.id
    assert fetched.telegram_id == 654321


@pytest.mark.asyncio
async def test_get_user_not_found(db_session: AsyncSession) -> None:
    with pytest.raises(HTTPException) as exc:
        await UserService.get_user(db_session, "00000000-0000-0000-0000-000000000000")
    assert exc.value.status_code == 404
    assert exc.value.detail == "User not found"


@pytest.mark.asyncio
async def test_list_users(db_session: AsyncSession) -> None:
    # Создаём двух пользователей
    user1 = await UserService.create_user(db_session, UserCreate(
        telegram_id=111111,
        first_name="First",
        last_name="User",
        status="student",
        role="user"
    ))
    user2 = await UserService.create_user(db_session, UserCreate(
        telegram_id=222222,
        first_name="Second",
        last_name="User",
        status="student",
        role="user"
    ))

    users = await UserService.list_users(db_session)
    ids = {u.id for u in users}
    assert user1.id in ids
    assert user2.id in ids
    assert len(users) >= 2
