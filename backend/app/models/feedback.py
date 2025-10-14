from sqlalchemy import ForeignKey, SmallInteger, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from app.models.base import Base


class Feedback(Base):
    __tablename__ = "feedback"

    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    rating: Mapped[int] = mapped_column(SmallInteger)
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    chat = relationship("Chat", back_populates="feedbacks")
    user = relationship("User", back_populates="feedbacks")
