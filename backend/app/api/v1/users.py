from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_session
from app.models.user import User
from app.schemas.user import UserCreate, UserRead

router = APIRouter()


@router.post("/", response_model=UserRead, summary="Создать пользователя")
async def create_user(
        user_in: UserCreate,
        session: AsyncSession = Depends(get_session),
) -> UserRead:
    user = User(**user_in.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return UserRead.model_validate(user)


@router.get("/{user_id}", response_model=UserRead, summary="Получить пользователя по ID")
async def get_user(
        user_id: str,
        session: AsyncSession = Depends(get_session),
) -> UserRead:
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserRead.model_validate(user)


@router.get("/", response_model=list[UserRead], summary="Список пользователей")
async def list_users(
        session: AsyncSession = Depends(get_session),
) -> List[UserRead]:
    result = await session.execute(select(User))
    users = result.scalars().all()
    return [UserRead.model_validate(user) for user in users]
