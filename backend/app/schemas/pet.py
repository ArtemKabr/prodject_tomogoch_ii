# backend/app/schemas/pet.py — Pydantic схемы питомца
"""
Схемы ответа по питомцу.
"""

from datetime import datetime

from pydantic import BaseModel


class PetOut(BaseModel):
    """Состояние питомца."""
    id: int
    age_stage: str
    health: int
    energy: int
    mood: int
    intellect: int
    bond: int
    is_alive: bool
    last_active_at: datetime
    created_at: datetime
    died_at: datetime | None
