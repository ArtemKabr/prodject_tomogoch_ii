# backend/app/services/pet_rules.py — правила игры для питомца
"""
Правила изменения параметров питомца: стадия, деградация, инкременты.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from app.models.pet import AgeStage, Pet


@dataclass(frozen=True)
class DegradationResult:
    """Результат деградации по времени."""

    hours_passed: int
    died_now: bool


def clamp_0_100(value: int) -> int:
    """Ограничить значение диапазоном 0..100."""
    return max(0, min(100, value))


def compute_stage(intellect: int) -> str:
    """Определить стадию по интеллекту."""
    if intellect >= 80:
        return AgeStage.mentor.value
    if intellect >= 50:
        return AgeStage.adult.value
    if intellect >= 20:
        return AgeStage.teen.value
    return AgeStage.baby.value


def apply_action_from_user_message(pet: Pet) -> None:
    """Применить изменения параметров от сообщения пользователя."""
    pet.bond = clamp_0_100(pet.bond + 2)  # (я добавил)
    pet.intellect = clamp_0_100(pet.intellect + 1)  # (я добавил)
    pet.energy = clamp_0_100(pet.energy + 1)  # (я добавил)
    pet.mood = clamp_0_100(pet.mood + 1)  # (я добавил)

    pet.age_stage = compute_stage(pet.intellect)  # (я добавил)
    pet.last_active_at = datetime.now(timezone.utc)  # (я добавил)


def apply_passive_degradation(pet: Pet, now: datetime | None = None) -> DegradationResult:
    """Деградировать питомца по времени простоя (вызов на /pet и /chat)."""
    if now is None:
        now = datetime.now(timezone.utc)

    if not pet.is_alive:
        return DegradationResult(hours_passed=0, died_now=False)

    last = pet.last_active_at
    if last.tzinfo is None:
        last = last.replace(tzinfo=timezone.utc)

    delta_hours = int((now - last).total_seconds() // 3600)
    if delta_hours <= 0:
        return DegradationResult(hours_passed=0, died_now=False)

    # MVP-формула: за каждый час -1 energy, -1 mood; после 24 часов дополнительно -1 health за час  # (я добавил)
    pet.energy = clamp_0_100(pet.energy - delta_hours)  # (я добавил)
    pet.mood = clamp_0_100(pet.mood - delta_hours)  # (я добавил)

    if delta_hours > 24:
        pet.health = clamp_0_100(pet.health - (delta_hours - 24))  # (я добавил)

    died_now = False
    if pet.health <= 0:
        pet.is_alive = False  # (я добавил)
        pet.died_at = now  # (я добавил)
        died_now = True  # (я добавил)

    return DegradationResult(hours_passed=delta_hours, died_now=died_now)
