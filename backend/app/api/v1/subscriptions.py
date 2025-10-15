from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db.session import get_session
from app.models.subscription import Subscription
from app.schemas.subscription import SubscriptionCreate, SubscriptionRead

router = APIRouter()


@router.post("/", response_model=SubscriptionRead, summary="Создать подписку")
async def create_subscription(
    sub_in: SubscriptionCreate,
    session: AsyncSession = Depends(get_session),
) -> SubscriptionRead:
    subscription = Subscription(**sub_in.model_dump())
    session.add(subscription)
    await session.commit()
    await session.refresh(subscription)
    return SubscriptionRead.model_validate(subscription)


@router.get("/{subscription_id}", response_model=SubscriptionRead, summary="Получить подписку по ID")
async def get_subscription(
    subscription_id: str,
    session: AsyncSession = Depends(get_session),
) -> SubscriptionRead:
    result = await session.execute(select(Subscription).where(Subscription.id == subscription_id))
    subscription = result.scalar_one_or_none()
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return SubscriptionRead.model_validate(subscription)


@router.get("/", response_model=list[SubscriptionRead], summary="Список подписок")
async def list_subscriptions(
    session: AsyncSession = Depends(get_session),
) -> List[SubscriptionRead]:
    result = await session.execute(select(Subscription))
    subscriptions = result.scalars().all()
    return [SubscriptionRead.model_validate(sub) for sub in subscriptions]