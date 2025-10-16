from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from app.models.chat import Chat, Message
from app.schemas.chat import ChatCreate


class ChatService:
    @staticmethod
    async def create_chat(session: AsyncSession, chat_in: ChatCreate) -> Chat:
        """
        Создать новый чат.
        """
        chat = Chat(**chat_in.model_dump())
        session.add(chat)
        await session.commit()
        await session.refresh(chat)
        return chat

    @staticmethod
    async def get_chat(session: AsyncSession, chat_id: str) -> Chat:
        """
        Получить чат по ID.
        """
        result = await session.execute(select(Chat).where(Chat.id == chat_id))
        chat: Optional[Chat] = result.scalar_one_or_none()
        if chat is None:
            raise HTTPException(status_code=404, detail="Chat not found")
        return chat

    @staticmethod
    async def list_chats(session: AsyncSession) -> List[Chat]:
        """
        Получить список всех чатов.
        """
        result = await session.execute(select(Chat))
        return list(result.scalars().all())

    @staticmethod
    async def list_messages(session: AsyncSession, chat_id: str) -> List[Message]:
        """
        Получить список сообщений для конкретного чата.
        """
        result = await session.execute(select(Message).where(Message.chat_id == chat_id))
        return list(result.scalars().all())
