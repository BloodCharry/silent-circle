from sqlalchemy import Enum, ForeignKey, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
from backend.app.models.base import Base


class ApplicationStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class Application(Base):
    __tablename__ = "applications"

    user_id: Mapped = mapped_column(ForeignKey("users.id"), unique=True)
    status: Mapped[ApplicationStatus] = mapped_column(default=ApplicationStatus.pending)
    submitted_at: Mapped = mapped_column(DateTime(timezone=True))
    reviewed_at: Mapped | None = mapped_column(DateTime(timezone=True), nullable=True)
    review_comment: Mapped[str | None] = mapped_column(Text, nullable=True)

    user = relationship("User", back_populates="application")
