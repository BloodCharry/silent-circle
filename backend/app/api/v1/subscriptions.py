from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_session
from app.schemas.subscription import SubscriptionCreate, SubscriptionRead
from app.services.subscription_service import SubscriptionService

router = APIRouter()


@router.post("/", response_model=SubscriptionRead, summary="Создать подписку")
async def create_subscription(
        sub_in: SubscriptionCreate,
        session: AsyncSession = Depends(get_session),
) -> SubscriptionRead:
    subscription = await SubscriptionService.create_subscription(session, sub_in)
    return SubscriptionRead.model_validate(subscription)


@router.get("/{subscription_id}", response_model=SubscriptionRead, summary="Получить подписку по ID")
async def get_subscription(
        subscription_id: str,
        session: AsyncSession = Depends(get_session),
) -> SubscriptionRead:
    subscription = await SubscriptionService.get_subscription(session, subscription_id)
    return SubscriptionRead.model_validate(subscription)


@router.get("/", response_model=List[SubscriptionRead], summary="Список подписок")
async def list_subscriptions(
        session: AsyncSession = Depends(get_session),
) -> List[SubscriptionRead]:
    subscriptions = await SubscriptionService.list_subscriptions(session)
    return [SubscriptionRead.model_validate(sub) for sub in subscriptions]
