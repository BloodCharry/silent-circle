from __future__ import annotations

from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from app.models.application import Application
from app.schemas.application import ApplicationCreate


class ApplicationService:
    @staticmethod
    async def create_application(session: AsyncSession, app_in: ApplicationCreate) -> Application:
        """
        Создаёт новую заявку в БД.
        - Принимает Pydantic-схему ApplicationCreate.
        - Возвращает ORM-модель Application после сохранения.
        """
        application = Application(**app_in.model_dump())
        session.add(application)
        await session.commit()
        await session.refresh(application)
        return application

    @staticmethod
    async def get_application(session: AsyncSession, application_id: str) -> Application:
        """
        Получает заявку по ID.
        - Если не найдена, выбрасывает HTTPException(404).
        """
        result = await session.execute(select(Application).where(Application.id == application_id))
        application: Application | None = result.scalar_one_or_none()
        if application is None:
            raise HTTPException(status_code=404, detail="Application not found")
        return application

    @staticmethod
    async def list_applications(session: AsyncSession) -> Sequence[Application]:
        """
        Возвращает список всех заявок.
        """
        result = await session.execute(select(Application))
        return result.scalars().all()
