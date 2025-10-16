from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from app.models.subscription import Subscription
from app.schemas.subscription import SubscriptionCreate


class SubscriptionService:
    @staticmethod
    async def create_subscription(session: AsyncSession, sub_in: SubscriptionCreate) -> Subscription:
        """
        Создать новую подписку.
        """
        subscription = Subscription(**sub_in.model_dump())
        session.add(subscription)
        await session.commit()
        await session.refresh(subscription)
        return subscription

    @staticmethod
    async def get_subscription(session: AsyncSession, subscription_id: str) -> Subscription:
        """
        Получить подписку по ID.
        """
        result = await session.execute(select(Subscription).where(Subscription.id == subscription_id))
        subscription: Optional[Subscription] = result.scalar_one_or_none()
        if subscription is None:
            raise HTTPException(status_code=404, detail="Subscription not found")
        return subscription

    @staticmethod
    async def list_subscriptions(session: AsyncSession) -> List[Subscription]:
        """
        Получить список всех подписок.
        """
        result = await session.execute(select(Subscription))
        return list(result.scalars().all())
