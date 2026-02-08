# backend/app/schemas/pet_action.py — схемы действий питомца

"""
Pydantic-схемы для действий питомца (кормить/гулять/играть/спать/тренировать).
"""

from pydantic import BaseModel, Field


class PetActionIn(BaseModel):
    """Запрос на действие питомца."""
    action: str = Field(  # (я добавил)
        pattern="^(feed|walk|play|sleep|train)$",  # (я добавил)
        description="Действие: feed|walk|play|sleep|train",  # (я добавил)
    )  # (я добавил)


class PetActionOut(BaseModel):
    """Ответ на действие питомца."""
    message: str  # (я добавил)
    pet_state: dict  # (я добавил) PetOut.model_dump(), позже типизировать


class PetStatusOut(BaseModel):
    """Расширенный статус для UI (подсказки/день-ночь/needs)."""
    time_of_day: str  # (я добавил) day|night
    needs: list[str]  # (я добавил)
    available_actions: list[str]  # (я добавил)
    pet_state: dict  # (я добавил) PetOut.model_dump()
