from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_session
from app.schemas.chat import ChatCreate, ChatRead, MessageRead
from app.services.chat_service import ChatService

router = APIRouter()


@router.post("/", response_model=ChatRead, summary="Создать чат")
async def create_chat(
        chat_in: ChatCreate,
        session: AsyncSession = Depends(get_session),
) -> ChatRead:
    chat = await ChatService.create_chat(session, chat_in)
    return ChatRead.model_validate(chat)


@router.get("/{chat_id}", response_model=ChatRead, summary="Получить чат по ID")
async def get_chat(
        chat_id: str,
        session: AsyncSession = Depends(get_session),
) -> ChatRead:
    chat = await ChatService.get_chat(session, chat_id)
    return ChatRead.model_validate(chat)


@router.get("/", response_model=List[ChatRead], summary="Список чатов")
async def list_chats(
        session: AsyncSession = Depends(get_session),
) -> List[ChatRead]:
    chats = await ChatService.list_chats(session)
    return [ChatRead.model_validate(chat) for chat in chats]


@router.get("/{chat_id}/messages", response_model=List[MessageRead], summary="Сообщения чата")
async def list_messages(
        chat_id: str,
        session: AsyncSession = Depends(get_session),
) -> List[MessageRead]:
    messages = await ChatService.list_messages(session, chat_id)
    return [MessageRead.model_validate(msg) for msg in messages]
