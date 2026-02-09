# backend/app/schemas/pet_action.py

from pydantic import BaseModel, Field
from typing import Any, Dict

class PetActionIn(BaseModel):
    action: str = Field(
        pattern="^(feed|walk|play|sleep|train)$",
        description="Действие: feed|walk|play|sleep|train",
    )

class PetActionOut(BaseModel):
    message: str
    pet_state: dict

class PetStatusOut(BaseModel):
    time_of_day: str
    needs: list[str]
    available_actions: list[str]
    cooldowns: dict[str, int]
    daily_quests: Dict[str, Any]
    streaks: Dict[str, Any]
    personality: str | None
    pet_state: dict
