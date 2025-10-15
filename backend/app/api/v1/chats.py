from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db.session import get_session
from app.models.chat import Chat, Message
from app.schemas.chat import ChatCreate, ChatRead, MessageRead

router = APIRouter()


@router.post("/", response_model=ChatRead, summary="Создать чат")
async def create_chat(
    chat_in: ChatCreate,
    session: AsyncSession = Depends(get_session),
) -> ChatRead:
    chat = Chat(**chat_in.model_dump())
    session.add(chat)
    await session.commit()
    await session.refresh(chat)
    return ChatRead.model_validate(chat)


@router.get("/{chat_id}", response_model=ChatRead, summary="Получить чат по ID")
async def get_chat(
    chat_id: str,
    session: AsyncSession = Depends(get_session),
) -> ChatRead:
    result = await session.execute(select(Chat).where(Chat.id == chat_id))
    chat = result.scalar_one_or_none()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return ChatRead.model_validate(chat)


@router.get("/", response_model=list[ChatRead], summary="Список чатов")
async def list_chats(
    session: AsyncSession = Depends(get_session),
) -> List[ChatRead]:
    result = await session.execute(select(Chat))
    chats = result.scalars().all()
    return [ChatRead.model_validate(chat) for chat in chats]


@router.get("/{chat_id}/messages", response_model=list[MessageRead], summary="Сообщения чата")
async def list_messages(
    chat_id: str,
    session: AsyncSession = Depends(get_session),
) -> List[MessageRead]:
    result = await session.execute(select(Message).where(Message.chat_id == chat_id))
    messages = result.scalars().all()
    return [MessageRead.model_validate(msg) for msg in messages]