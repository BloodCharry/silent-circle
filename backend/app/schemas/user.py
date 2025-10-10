from pydantic import BaseModel, Field
from typing import Optional
import uuid
from datetime import datetime
from app.models.user import UserStatus, UserRole  # type: ignore


class UserBase(BaseModel):
    first_name: str
    last_name: str
    status: UserStatus
    about: Optional[str] = None
    interests: Optional[dict] = None
    avatar_url: Optional[str] = None


class UserCreate(UserBase):
    telegram_id: int


class UserRead(UserBase):
    id: uuid.UUID
    role: UserRole
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
