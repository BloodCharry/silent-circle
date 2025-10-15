from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas.user import UserCreate, UserRead
from app.services.user_service import UserService

router = APIRouter()


@router.post("/", response_model=UserRead, summary="Создать пользователя")
async def create_user(
    user_in: UserCreate,
    session: AsyncSession = Depends(get_session),
) -> UserRead:
    user = await UserService.create_user(session, user_in)
    return UserRead.model_validate(user)


@router.get("/{user_id}", response_model=UserRead, summary="Получить пользователя по ID")
async def get_user(
    user_id: str,
    session: AsyncSession = Depends(get_session),
) -> UserRead:
    user = await UserService.get_user(session, user_id)
    return UserRead.model_validate(user)


@router.get("/", response_model=List[UserRead], summary="Список пользователей")
async def list_users(
    session: AsyncSession = Depends(get_session),
) -> List[UserRead]:
    users = await UserService.list_users(session)
    return [UserRead.model_validate(user) for user in users]
