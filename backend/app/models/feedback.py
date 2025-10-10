from sqlalchemy import ForeignKey, SmallInteger, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.models.base import Base


class Feedback(Base):
    __tablename__ = "feedback"

    chat_id: Mapped = mapped_column(ForeignKey("chats.id"))
    user_id: Mapped = mapped_column(ForeignKey("users.id"))
    rating: Mapped[int] = mapped_column(SmallInteger)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)

    chat = relationship("Chat", back_populates="feedbacks")
    user = relationship("User", back_populates="feedbacks")
