from sqlalchemy import String, Enum, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
from backend.app.models.base import Base


class UserStatus(str, enum.Enum):
    student = "student"
    worker = "worker"
    entrepreneur = "entrepreneur"
    researcher = "researcher"


class UserRole(str, enum.Enum):
    user = "user"
    admin = "admin"
    moderator = "moderator"


class User(Base):
    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(unique=True, index=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    status: Mapped[UserStatus]
    about: Mapped[str | None] = mapped_column(Text, nullable=True)
    interests: Mapped[dict | None] = mapped_column(nullable=True)  # JSONB
    avatar_url: Mapped[str | None] = mapped_column(String, nullable=True)
    role: Mapped[UserRole] = mapped_column(default=UserRole.user)

    # relations
    application = relationship("Application", back_populates="user", uselist=False)
    subscriptions = relationship("Subscription", back_populates="user")
    chat_memberships = relationship("ChatMember", back_populates="user")
    feedbacks = relationship("Feedback", back_populates="user")
