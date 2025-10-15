from sqlalchemy import Enum, ForeignKey, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
from datetime import datetime
from typing import Optional
from app.models.base import Base


class SubscriptionStatus(str, enum.Enum):
    trial = "trial"
    active = "active"
    expired = "expired"
    canceled = "canceled"


class SubscriptionPlan(str, enum.Enum):
    monthly = "monthly"
    half_year = "half_year"
    yearly = "yearly"


class Subscription(Base):
    __tablename__ = "subscriptions"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    status: Mapped[SubscriptionStatus] = mapped_column(Enum(SubscriptionStatus))
    plan: Mapped[SubscriptionPlan] = mapped_column(Enum(SubscriptionPlan))
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    payment_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    user = relationship("User", back_populates="subscriptions")
