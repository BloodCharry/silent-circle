from __future__ import annotations

from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from app.models.user import User
from app.schemas.user import UserCreate


class UserService:
    @staticmethod
    async def create_user(session: AsyncSession, user_in: UserCreate) -> User:
        """
        Создаёт нового пользователя в БД.
        - Принимает Pydantic-схему UserCreate.
        - Возвращает ORM-модель User после сохранения.
        """
        user = User(**user_in.model_dump())
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    @staticmethod
    async def get_user(session: AsyncSession, user_id: str) -> User:
        """
        Получает пользователя по ID.
        - Если пользователь не найден, выбрасывает HTTPException(404).
        """
        result = await session.execute(select(User).where(User.id == user_id))
        user: User | None = result.scalar_one_or_none()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    @staticmethod
    async def list_users(session: AsyncSession) -> Sequence[User]:
        """
        Возвращает список всех пользователей.
        """
        result = await session.execute(select(User))
        return result.scalars().all()