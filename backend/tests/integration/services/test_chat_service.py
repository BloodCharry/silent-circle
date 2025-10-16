import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.chat_service import ChatService
from app.schemas.chat import ChatCreate
from app.models.chat import Chat, Message
from app.models.user import User


@pytest.mark.asyncio
class TestChatService:
    async def test_create_chat(self, db_session: AsyncSession) -> None:
        chat_in = ChatCreate(is_active=True)
        chat: Chat = await ChatService.create_chat(db_session, chat_in)
        assert isinstance(chat, Chat)
        assert chat.is_active is True
        assert chat.id is not None

    async def test_get_chat_not_found(self, db_session: AsyncSession) -> None:
        with pytest.raises(Exception) as exc:
            await ChatService.get_chat(db_session, "00000000-0000-0000-0000-000000000000")
        assert "Chat not found" in str(exc.value)

    async def test_list_chats(self, db_session: AsyncSession) -> None:
        for _ in range(2):
            await ChatService.create_chat(db_session, ChatCreate(is_active=True))

        chats = await ChatService.list_chats(db_session)
        assert len(chats) == 2
        assert all(isinstance(c, Chat) for c in chats)

    async def test_list_messages_empty(self, db_session: AsyncSession) -> None:
        chat = await ChatService.create_chat(db_session, ChatCreate(is_active=True))
        messages = await ChatService.list_messages(db_session, chat.id)
        assert messages == []
        assert isinstance(messages, list)

    async def test_list_messages_with_data(self, db_session: AsyncSession) -> None:
        chat = await ChatService.create_chat(db_session, ChatCreate(is_active=True))

        user = User(
            telegram_id=123456,
            first_name="Test",
            last_name="User",
            status="student",
            role="user"
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        message = Message(
            chat_id=chat.id,
            sender_id=user.id,
            content="Hello, world!",
        )
        db_session.add(message)
        await db_session.commit()
        await db_session.refresh(message)

        messages = await ChatService.list_messages(db_session, chat.id)
        assert len(messages) == 1
        assert messages[0].content == "Hello, world!"
        assert messages[0].chat_id == chat.id
        assert messages[0].sender_id == user.id
