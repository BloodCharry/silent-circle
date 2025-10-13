import pytest
from httpx import AsyncClient


class TestApplicationsAPI:
    async def _create_user(self, client: AsyncClient):
        user_resp = await client.post("/api/v1/users/", json={
            "telegram_id": 111111111,
            "first_name": "Test",
            "last_name": "User",
            "status": "student",
            "role": "user"
        })
        return user_resp.json()

    async def test_create_application_success(self, client: AsyncClient):
        user = await self._create_user(client)
        app_data = {
            "user_id": user["id"],
            "status": "pending",
            "review_comment": None
        }
        response = await client.post("/api/v1/applications/", json=app_data)
        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == user["id"]
        assert data["status"] == "pending"

    async def test_get_application_not_found(self, client: AsyncClient):
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = await client.get(f"/api/v1/applications/{fake_id}")
        assert response.status_code == 404
        assert response.json()["detail"] == "Application not found"

    async def test_list_applications_empty(self, client: AsyncClient):
        response = await client.get("/api/v1/applications/")
        assert response.status_code == 200
        assert response.json() == []
