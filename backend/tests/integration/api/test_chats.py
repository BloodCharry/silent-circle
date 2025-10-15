import pytest
from httpx import AsyncClient
from typing import Any


class TestChatsAPI:
    async def test_create_chat_success(self, client: AsyncClient) -> None:
        chat_data: dict[str, Any] = {"is_active": True}
        response = await client.post("/api/v1/chats/", json=chat_data)
        assert response.status_code == 200
        data: dict[str, Any] = response.json()
        assert "id" in data
        assert data["is_active"] is True

    async def test_get_chat_not_found(self, client: AsyncClient) -> None:
        fake_id: str = "00000000-0000-0000-0000-000000000000"
        response = await client.get(f"/api/v1/chats/{fake_id}")
        assert response.status_code == 404
        detail: str = response.json()["detail"]
        assert detail == "Chat not found"

    async def test_list_chats_empty(self, client: AsyncClient) -> None:
        response = await client.get("/api/v1/chats/")
        assert response.status_code == 200
        data: list[dict[str, Any]] = response.json()
        assert data == []

    async def test_list_chats_with_data(self, client: AsyncClient) -> None:
        chats: list[dict[str, Any]] = []
        for _ in range(2):
            resp = await client.post("/api/v1/chats/", json={"is_active": True})
            chats.append(resp.json())

        response = await client.get("/api/v1/chats/")
        assert response.status_code == 200
        data: list[dict[str, Any]] = response.json()
        assert len(data) == 2
        assert {c["id"] for c in data} == {c["id"] for c in chats}

    async def test_list_messages_empty(self, client: AsyncClient) -> None:
        # создаём чат
        resp = await client.post("/api/v1/chats/", json={"is_active": True})
        chat: dict[str, Any] = resp.json()

        # проверяем, что сообщений нет
        response = await client.get(f"/api/v1/chats/{chat['id']}/messages")
        assert response.status_code == 200
        messages: list[dict[str, Any]] = response.json()
        assert messages == []
