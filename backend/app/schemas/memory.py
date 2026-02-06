# backend/app/schemas/memory.py — Pydantic схемы памяти
"""
Схемы для памяти пользователя.
"""

from datetime import datetime

from pydantic import BaseModel, Field


class MemoryIn(BaseModel):
    """Добавление записи памяти."""
    type: str = Field(pattern="^(profile|preference|shared_story)$")
    text: str = Field(min_length=1, max_length=2000)
    importance: int = Field(ge=1, le=5, default=3)


class MemoryOut(BaseModel):
    """Запись памяти."""
    id: int
    type: str
    text: str
    importance: int
    created_at: datetime
    updated_at: datetime | None
