# backend/app/schemas/chat.py — Pydantic схемы чата
"""
Схемы для отправки сообщений и ответа.
"""

from pydantic import BaseModel, Field


class ChatIn(BaseModel):
    """Запрос в чат."""
    conversation_id: int | None = None
    message: str = Field(min_length=1, max_length=5000)


class ChatOut(BaseModel):
    """Ответ чата."""
    assistant_message: str
    stage: str
    conversation_id: int
    pet_state: dict  # (я добавил) на MVP можно вернуть PetOut.model_dump(), позже типизировать
