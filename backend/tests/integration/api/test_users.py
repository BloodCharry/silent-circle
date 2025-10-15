import uuid
import pytest
from httpx import AsyncClient
from app.models.user import UserStatus, UserRole


class TestUsersAPI:

    async def test_create_user_success(self, client: AsyncClient) -> None:
        user_data = {
            "telegram_id": 123456789,
            "first_name": "Иван",
            "last_name": "Иванов",
            "status": UserStatus.student.value,
            "about": "Люблю читать",
            "interests": {"hobbies": ["books", "coding"]},
            "role": UserRole.user.value,
        }
        response = await client.post("/api/v1/users/", json=user_data)
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert data["telegram_id"] == 123456789
        assert isinstance(uuid.UUID(data["id"]), uuid.UUID)

    async def test_get_user_not_found(self, client: AsyncClient) -> None:
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = await client.get(f"/api/v1/users/{fake_id}")
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"

    async def test_list_users_empty(self, client: AsyncClient) -> None:
        response = await client.get("/api/v1/users/")
        assert response.status_code == 200
        assert response.json() == []

    async def test_list_users_with_data(self, client: AsyncClient) -> None:
        users = []
        for i in range(2):
            resp = await client.post("/api/v1/users/", json={
                "telegram_id": 1000 + i,
                "first_name": f"User{i}",
                "last_name": "Test",
                "status": UserStatus.student.value,
                "role": UserRole.user.value,
            })
            users.append(resp.json())

        response = await client.get("/api/v1/users/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert {u["id"] for u in data} == {u["id"] for u in users}