from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_session
from app.models.application import Application
from app.schemas.application import ApplicationCreate, ApplicationRead

router = APIRouter()


@router.post("/", response_model=ApplicationRead, summary="Создать заявку")
async def create_application(
        app_in: ApplicationCreate,
        session: AsyncSession = Depends(get_session),
) -> ApplicationRead:
    application = Application(**app_in.model_dump())
    session.add(application)
    await session.commit()
    await session.refresh(application)
    return ApplicationRead.model_validate(application)


@router.get("/{application_id}", response_model=ApplicationRead, summary="Получить заявку по ID")
async def get_application(application_id: str, session: AsyncSession = Depends(get_session)) -> ApplicationRead:
    result = await session.execute(select(Application).where(Application.id == application_id))
    application = result.scalar_one_or_none()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return ApplicationRead.model_validate(application)


@router.get("/", response_model=list[ApplicationRead], summary="Список заявок")
async def list_applications(session: AsyncSession = Depends(get_session)) -> List[ApplicationRead]:
    result = await session.execute(select(Application))
    applications = result.scalars().all()
    return [ApplicationRead.model_validate(app) for app in applications]
