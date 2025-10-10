from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime


class ChatBase(BaseModel):
    is_active: bool = True


class ChatCreate(ChatBase):
    pass


class ChatRead(ChatBase):
    id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True


class MessageRead(BaseModel):
    id: uuid.UUID
    chat_id: uuid.UUID
    sender_id: uuid.UUID
    content: str
    created_at: datetime

    class Config:
        from_attributes = True
