from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime
from app.models.subscription import SubscriptionStatus, SubscriptionPlan  # type: ignore


class SubscriptionBase(BaseModel):
    status: SubscriptionStatus
    plan: SubscriptionPlan


class SubscriptionCreate(SubscriptionBase):
    user_id: uuid.UUID
    started_at: datetime
    expires_at: datetime
    payment_id: Optional[str] = None


class SubscriptionRead(SubscriptionBase):
    id: uuid.UUID
    user_id: uuid.UUID
    started_at: datetime
    expires_at: datetime
    payment_id: Optional[str]

    class Config:
        from_attributes = True
