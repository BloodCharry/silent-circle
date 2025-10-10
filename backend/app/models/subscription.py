from sqlalchemy import Enum, ForeignKey, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
from backend.app.models.base import Base


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

    user_id: Mapped = mapped_column(ForeignKey("users.id"))
    status: Mapped[SubscriptionStatus]
    plan: Mapped[SubscriptionPlan]
    started_at: Mapped
    expires_at: Mapped
    payment_id: Mapped[str | None] = mapped_column(String, nullable=True)

    user = relationship("User", back_populates="subscriptions")
