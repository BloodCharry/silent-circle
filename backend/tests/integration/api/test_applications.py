from typing import Dict, Any
import pytest
from httpx import AsyncClient

from app.models.user import UserStatus, UserRole
from app.models.application import ApplicationStatus


class TestApplicationsAPI:
    async def _create_user(self, client: AsyncClient, idx: int = 0) -> Dict[str, Any]:
        user_resp = await client.post("/api/v1/users/", json={
            "telegram_id": 111111111 + idx,
            "first_name": f"Test{idx}",
            "last_name": "User",
            "status": UserStatus.student.value,
            "role": UserRole.user.value,
        })
        data = user_resp.json()
        assert isinstance(data, dict), f"Expected dict, got {type(data)}"
        return data

    async def test_create_application_success(self, client: AsyncClient) -> None:
        user = await self._create_user(client, idx=0)
        app_data = {
            "user_id": user["id"],
            "status": ApplicationStatus.pending.value,
            "review_comment": None,
        }
        response = await client.post("/api/v1/applications/", json=app_data)
        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == user["id"]
        assert data["status"] == ApplicationStatus.pending.value

    async def test_get_application_not_found(self, client: AsyncClient) -> None:
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = await client.get(f"/api/v1/applications/{fake_id}")
        assert response.status_code == 404
        assert response.json()["detail"] == "Application not found"

    async def test_list_applications_empty(self, client: AsyncClient) -> None:
        response = await client.get("/api/v1/applications/")
        assert response.status_code == 200
        assert response.json() == []

    async def test_list_applications_with_data(self, client: AsyncClient) -> None:
        apps = []
        for i in range(2):
            user = await self._create_user(client, idx=i)
            resp = await client.post("/api/v1/applications/", json={
                "user_id": user["id"],
                "status": ApplicationStatus.pending.value,
                "review_comment": f"Test comment {i}",
            })
            assert resp.status_code == 200
            apps.append(resp.json())

        response = await client.get("/api/v1/applications/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert {a["id"] for a in data} == {a["id"] for a in apps}
