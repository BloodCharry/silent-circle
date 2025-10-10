from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime
from app.models.application import ApplicationStatus  # type: ignore


class ApplicationBase(BaseModel):
    status: ApplicationStatus


class ApplicationCreate(BaseModel):
    user_id: uuid.UUID


class ApplicationRead(ApplicationBase):
    id: uuid.UUID
    user_id: uuid.UUID
    submitted_at: datetime
    reviewed_at: Optional[datetime]
    review_comment: Optional[str]

    class Config:
        from_attributes = True
