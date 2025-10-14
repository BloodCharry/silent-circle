from sqlalchemy import Enum, ForeignKey, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

import enum
from datetime import datetime
from typing import Optional
from app.models.base import Base


class ApplicationStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class Application(Base):
    __tablename__ = "applications"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    status: Mapped[ApplicationStatus] = mapped_column(Enum(ApplicationStatus), default=ApplicationStatus.pending)
    submitted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    reviewed_at: Mapped[Optional[datetime]]
    review_comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    user = relationship("User", back_populates="application")
