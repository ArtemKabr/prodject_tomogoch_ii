
# backend/app/models/conversation.py — диалоги и сообщения
"""
Conversations и Messages для чата.
"""

from datetime import datetime
from enum import StrEnum

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class MessageRole(StrEnum):
    """Роли сообщений в диалоге."""

    user = "user"
    assistant = "assistant"


class Conversation(Base):
    """Диалог пользователя с питомцем."""

    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), index=True, nullable=False)
    pet_id: Mapped[int] = mapped_column(Integer, ForeignKey("pets.id"), index=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    pet = relationship("Pet", back_populates="conversations")  # (я добавил)
    messages = relationship("Message", back_populates="conversation", order_by="Message.created_at")  # (я добавил)


class Message(Base):
    """Сообщение в диалоге."""

    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    conversation_id: Mapped[int] = mapped_column(Integer, ForeignKey("conversations.id"), index=True, nullable=False)

    role: Mapped[str] = mapped_column(String(16), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    conversation = relationship("Conversation", back_populates="messages")  # (я добавил)
