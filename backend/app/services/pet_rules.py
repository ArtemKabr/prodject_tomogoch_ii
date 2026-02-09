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


def apply_action_from_user_message(pet: Pet, *, user_text: str = "") -> None:  # (я добавил)
    """Применить изменения параметров от сообщения пользователя."""  # (я добавил)
    # базовый позитив за взаимодействие (как было)  # (я добавил)
    bond_delta = 2  # (я добавил)
    intellect_delta = 1  # (я добавил)
    energy_delta = 1  # (я добавил)
    mood_delta = 1  # (я добавил)

    t = (user_text or "").strip()  # (я добавил)
    tl = t.lower()  # (я добавил)

    # вопрос: чуть больше интеллекта, чуть меньше энергии  # (я добавил)
    if tl.endswith("?"):  # (я добавил)
        intellect_delta += 1  # (я добавил)
        energy_delta -= 1  # (я добавил)

    # поддержка/похвала  # (я добавил)
    if any(x in tl for x in ("спасибо", "молодец", "умница", "ты классный", "классно")):  # (я добавил)
        mood_delta += 2  # (я добавил)
        bond_delta += 2  # (я добавил)

    # агрессия/токсичность (очень грубо, MVP)  # (я добавил)
    if any(x in tl for x in ("идиот", "тупой", "ненавижу тебя", "пошел", "сука")):  # (я добавил)
        mood_delta -= 4  # (я добавил)
        bond_delta -= 3  # (я добавил)

    pet.bond = clamp_0_100(pet.bond + bond_delta)  # (я добавил)
    pet.intellect = clamp_0_100(pet.intellect + intellect_delta)  # (я добавил)
    pet.energy = clamp_0_100(pet.energy + energy_delta)  # (я добавил)
    pet.mood = clamp_0_100(pet.mood + mood_delta)  # (я добавил)

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


# === ДЕЙСТВИЯ ТАМАГОЧИ (UI-кнопки) ===  # (я добавил)

@dataclass(frozen=True)
class ActionResult:  # (я добавил)
    """Результат применения действия (для UI и текста реакции)."""  # (я добавил)
    message: str  # (я добавил)
    time_of_day: str  # (я добавил) day|night
    available_actions: list[str]  # (я добавил)


def get_time_of_day(now: datetime) -> str:  # (я добавил)
    """Определить время суток (day|night) по часу (UTC)."""  # (я добавил)
    hour = now.hour  # (я добавил)
    # 06:00–21:59 — день, 22:00–05:59 — ночь  # (я добавил)
    return "day" if 6 <= hour < 22 else "night"  # (я добавил)


def get_available_actions(*, pet: Pet, now: datetime) -> list[str]:  # (я добавил)
    """Вернуть список доступных действий с учётом времени суток и состояния."""  # (я добавил)
    if not pet.is_alive:  # (я добавил)
        return []  # (я добавил)

    tod = get_time_of_day(now)  # (я добавил)
    actions: list[str] = ["feed", "play", "train", "walk", "sleep"]  # (я добавил)

    if tod == "night":  # (я добавил)
        # ночью нельзя гулять (и по желанию можно ограничить тренировки)  # (я добавил)
        actions = [a for a in actions if a != "walk"]  # (я добавил)
    else:  # (я добавил)
        # днём нельзя спать  # (я добавил)
        actions = [a for a in actions if a != "sleep"]  # (я добавил)

    # если энергии совсем нет — запретим активные действия, оставим корм/сон  # (я добавил)
    if pet.energy <= 5:  # (я добавил)
        actions = [a for a in actions if a in ("feed", "sleep")]  # (я добавил)

    return actions  # (я добавил)


def apply_action(*, pet: Pet, action: str, now: datetime | None = None) -> ActionResult:  # (я добавил)
    """Применить действие к питомцу и вернуть текст реакции + доступные действия."""  # (я добавил)
    if now is None:  # (я добавил)
        now = datetime.now(timezone.utc)  # (я добавил)

    tod = get_time_of_day(now)  # (я добавил)
    available = get_available_actions(pet=pet, now=now)  # (я добавил)

    if action not in available:  # (я добавил)
        return ActionResult(  # (я добавил)
            message="Сейчас это действие недоступно.",  # (я добавил)
            time_of_day=tod,  # (я добавил)
            available_actions=available,  # (я добавил)
        )  # (я добавил)

    # Эффекты действий (MVP, дальше будем балансить)  # (я добавил)
    if action == "feed":  # (я добавил)
        pet.health = clamp_0_100(pet.health + 6)  # (я добавил)
        pet.energy = clamp_0_100(pet.energy + 12)  # (я добавил)
        pet.mood = clamp_0_100(pet.mood + 2)  # (я добавил)
        msg = "Ням! Спасибо, стало лучше."  # (я добавил)
    elif action == "walk":  # (я добавил)
        pet.mood = clamp_0_100(pet.mood + 10)  # (я добавил)
        pet.energy = clamp_0_100(pet.energy - 10)  # (я добавил)
        pet.bond = clamp_0_100(pet.bond + 3)  # (я добавил)
        msg = "Классно погуляли, я прям ожил."  # (я добавил)
    elif action == "play":  # (я добавил)
        pet.mood = clamp_0_100(pet.mood + 12)  # (я добавил)
        pet.energy = clamp_0_100(pet.energy - 6)  # (я добавил)
        pet.bond = clamp_0_100(pet.bond + 5)  # (я добавил)
        msg = "Играем! Мне весело с тобой."  # (я добавил)
    elif action == "sleep":  # (я добавил)
        pet.energy = clamp_0_100(pet.energy + 25)  # (я добавил)
        pet.mood = clamp_0_100(pet.mood + 3)  # (я добавил)
        msg = "Спокойной ночи. Я набираюсь сил."  # (я добавил)
    elif action == "train":  # (я добавил)
        pet.intellect = clamp_0_100(pet.intellect + 4)  # (я добавил)
        pet.energy = clamp_0_100(pet.energy - 8)  # (я добавил)
        pet.mood = clamp_0_100(pet.mood - 1)  # (я добавил)
        msg = "Учусь! Чувствую, что становлюсь умнее."  # (я добавил)
    else:  # (я добавил)
        msg = "Окей."  # (я добавил)

    pet.age_stage = compute_stage(pet.intellect)  # (я добавил)
    pet.last_active_at = now  # (я добавил)

    available2 = get_available_actions(pet=pet, now=now)  # (я добавил)
    return ActionResult(message=msg, time_of_day=tod, available_actions=available2)  # (я добавил)
