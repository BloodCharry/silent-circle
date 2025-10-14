from pydantic import BaseModel, ConfigDict
from typing import Optional
import uuid
from datetime import datetime
from app.models.application import ApplicationStatus


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

    model_config = ConfigDict(from_attributes=True)
