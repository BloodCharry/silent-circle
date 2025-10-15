import pytest
from httpx import AsyncClient
from typing import Any, cast
import secrets
from datetime import datetime, timedelta, UTC

INT32_MAX = 2_147_483_647


class TestSubscriptionsAPI:
    async def _create_user(self, client: AsyncClient) -> dict[str, Any]:
        telegram_id: int = secrets.randbelow(INT32_MAX)

        user_data: dict[str, Any] = {
            "telegram_id": telegram_id,
            "first_name": "Sub",
            "last_name": "User",
            "status": "student",
            "role": "user"
        }
        response = await client.post("/api/v1/users/", json=user_data)
        assert response.status_code == 200
        return cast(dict[str, Any], response.json())

    async def _create_subscription(self, client: AsyncClient) -> dict[str, Any]:
        user = await self._create_user(client)
        sub_data: dict[str, Any] = {
            "status": "active",
            "plan": "monthly",
            "user_id": user["id"],
            "started_at": datetime.now(UTC).isoformat(),
            "expires_at": (datetime.now(UTC) + timedelta(days=30)).isoformat(),
            "payment_id": "pay_123"
        }
        response = await client.post("/api/v1/subscriptions/", json=sub_data)
        assert response.status_code == 200
        return cast(dict[str, Any], response.json())

    async def test_create_subscription_success(self, client: AsyncClient) -> None:
        subscription = await self._create_subscription(client)
        assert "id" in subscription
        assert subscription["plan"] == "monthly"
        assert subscription["status"] == "active"

    async def test_get_subscription_not_found(self, client: AsyncClient) -> None:
        fake_id: str = "00000000-0000-0000-0000-000000000000"
        response = await client.get(f"/api/v1/subscriptions/{fake_id}")
        assert response.status_code == 404
        assert response.json()["detail"] == "Subscription not found"

    async def test_list_subscriptions_empty(self, client: AsyncClient) -> None:
        response = await client.get("/api/v1/subscriptions/")
        assert response.status_code == 200
        data: list[dict[str, Any]] = response.json()
        assert data == []

    async def test_list_subscriptions_with_data(self, client: AsyncClient) -> None:
        subs: list[dict[str, Any]] = []
        for plan in ("monthly", "yearly"):
            user = await self._create_user(client)
            sub_data: dict[str, Any] = {
                "status": "active",
                "plan": plan,
                "user_id": user["id"],
                "started_at": datetime.now(UTC).isoformat(),
                "expires_at": (datetime.now(UTC) + timedelta(days=30)).isoformat(),
            }
            resp = await client.post("/api/v1/subscriptions/", json=sub_data)
            assert resp.status_code == 200
            subs.append(resp.json())

        response = await client.get("/api/v1/subscriptions/")
        assert response.status_code == 200
        data: list[dict[str, Any]] = response.json()
        assert len(data) == 2
        assert {s["id"] for s in data} == {s["id"] for s in subs}
