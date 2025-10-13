from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID
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
    role: Optional[UserRole] = UserRole.user


class UserRead(UserBase):
    id: UUID
    telegram_id: int
    role: UserRole
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
