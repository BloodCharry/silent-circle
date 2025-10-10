from sqlalchemy import Boolean, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.models.base import Base


class Chat(Base):
    __tablename__ = "chats"

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    members = relationship("ChatMember", back_populates="chat")
    messages = relationship("Message", back_populates="chat")
    feedbacks = relationship("Feedback", back_populates="chat")


class ChatMember(Base):
    __tablename__ = "chat_members"

    chat_id: Mapped = mapped_column(ForeignKey("chats.id"))
    user_id: Mapped = mapped_column(ForeignKey("users.id"))

    chat = relationship("Chat", back_populates="members")
    user = relationship("User", back_populates="chat_memberships")


class Message(Base):
    __tablename__ = "messages"

    chat_id: Mapped = mapped_column(ForeignKey("chats.id"))
    sender_id: Mapped = mapped_column(ForeignKey("users.id"))
    content: Mapped[str] = mapped_column(Text)

    chat = relationship("Chat", back_populates="messages")
