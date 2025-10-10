from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime


class FeedbackBase(BaseModel):
    rating: int
    comment: Optional[str] = None


class FeedbackCreate(FeedbackBase):
    chat_id: uuid.UUID
    user_id: uuid.UUID


class FeedbackRead(FeedbackBase):
    id: uuid.UUID
    chat_id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True
