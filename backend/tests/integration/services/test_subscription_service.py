import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta, UTC

from app.services.subscription_service import SubscriptionService
from app.schemas.subscription import SubscriptionCreate
from app.models.subscription import Subscription
from app.models.user import User


@pytest.mark.asyncio
class TestSubscriptionService:
    async def _create_user(self, db_session: AsyncSession) -> User:
        user = User(
            telegram_id=999999,
            first_name="Sub",
            last_name="Tester",
            status="student",
            role="user",
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        return user

    async def test_create_subscription(self, db_session: AsyncSession) -> None:
        user = await self._create_user(db_session)
        sub_in = SubscriptionCreate(
            status="active",
            plan="monthly",
            user_id=user.id,
            started_at=datetime.now(tz=UTC),
            expires_at=datetime.now(tz=UTC) + timedelta(days=30),
            payment_id="pay_123",
        )
        subscription: Subscription = await SubscriptionService.create_subscription(db_session, sub_in)
        assert isinstance(subscription, Subscription)
        assert subscription.plan == "monthly"
        assert subscription.status == "active"
        assert subscription.user_id == user.id

    async def test_get_subscription_not_found(self, db_session: AsyncSession) -> None:
        with pytest.raises(Exception) as exc:
            await SubscriptionService.get_subscription(db_session, "00000000-0000-0000-0000-000000000000")
        assert "Subscription not found" in str(exc.value)

    async def test_list_subscriptions(self, db_session: AsyncSession) -> None:
        user = await self._create_user(db_session)
        for plan in ("monthly", "yearly"):
            sub_in = SubscriptionCreate(
                status="active",
                plan=plan,
                user_id=user.id,
                started_at=datetime.now(tz=UTC),
                expires_at=datetime.now(tz=UTC) + timedelta(days=30),
                payment_id=f"pay_{plan}",
            )
            await SubscriptionService.create_subscription(db_session, sub_in)

        subs = await SubscriptionService.list_subscriptions(db_session)
        assert len(subs) == 2
        assert all(isinstance(s, Subscription) for s in subs)
