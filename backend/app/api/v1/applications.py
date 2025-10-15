from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas.application import ApplicationCreate, ApplicationRead
from app.services.application_service import ApplicationService

router = APIRouter()


@router.post("/", response_model=ApplicationRead, summary="Создать заявку")
async def create_application(
    app_in: ApplicationCreate,
    session: AsyncSession = Depends(get_session),
) -> ApplicationRead:
    application = await ApplicationService.create_application(session, app_in)
    return ApplicationRead.model_validate(application)


@router.get("/{application_id}", response_model=ApplicationRead, summary="Получить заявку по ID")
async def get_application(
    application_id: str,
    session: AsyncSession = Depends(get_session),
) -> ApplicationRead:
    application = await ApplicationService.get_application(session, application_id)
    return ApplicationRead.model_validate(application)


@router.get("/", response_model=List[ApplicationRead], summary="Список заявок")
async def list_applications(
    session: AsyncSession = Depends(get_session),
) -> List[ApplicationRead]:
    applications = await ApplicationService.list_applications(session)
    return [ApplicationRead.model_validate(app) for app in applications]
