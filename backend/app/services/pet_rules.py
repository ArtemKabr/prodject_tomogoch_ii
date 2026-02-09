# backend/app/services/pet_rules.py

from __future__ import annotations
import zoneinfo
import random
from dataclasses import dataclass
from datetime import datetime, time, timedelta, timezone

from app.models.pet import Pet

# ... (existing constants) ...

# Фаза 5: Константы
PERSONALITY_TRAITS = {
    "intellectual": lambda p: p.intellect > p.bond and p.intellect > p.mood,
    "social": lambda p: p.bond > p.intellect and p.bond > p.energy,
    "active": lambda p: p.energy > p.mood and p.energy > p.intellect,
    "balanced": lambda p: True, # Default
}

QUESTS_BY_PERSONALITY = {
    "intellectual": [{"action": "train", "target": 2, "reward": {"intellect": 10, "mood": 5}}],
    "social": [{"action": "play", "target": 3, "reward": {"bond": 10, "mood": 5}}],
    "active": [{"action": "walk", "target": 1, "reward": {"energy": 15, "health": 5}}],
    "balanced": [{"action": "feed", "target": 4, "reward": {"health": 10, "energy": 5}}],
}


def determine_personality(pet: Pet) -> str:
    """Определить характер питомца на основе его статов."""
    for trait, condition in PERSONALITY_TRAITS.items():
        if condition(pet):
            return trait
    return "balanced"

def generate_daily_quests(pet: Pet, now: datetime, user_tz: str):
    """Генерировать ежедневные квесты, если необходимо."""
    # Проверяем, наступил ли новый день по времени пользователя
    user_timezone = zoneinfo.ZoneInfo(user_tz)
    last_update_local = pet.updated_at.astimezone(user_timezone).date()
    now_local = now.astimezone(user_timezone).date()

    if now_local > last_update_local or not pet.daily_quests:
        personality = pet.personality_type or determine_personality(pet)
        pet.personality_type = personality
        
        possible_quests = QUESTS_BY_PERSONALITY.get(personality, []) 
        quest_template = random.choice(possible_quests)
        
        pet.daily_quests = {
            "quest_1": {
                "action": quest_template["action"],
                "target": quest_template["target"],
                "progress": 0,
                "completed": False,
                "reward": quest_template["reward"]
            }
        }

def update_streaks(pet: Pet, now: datetime):
    """Обновить серии (streaks) за ежедневный вход и выполнение квестов."""
    # Серия входов
    if (now.date() - pet.last_active_at.date()).days == 1:
        pet.streaks["login"] = pet.streaks.get("login", 0) + 1
    elif (now.date() - pet.last_active_at.date()).days > 1:
        pet.streaks["login"] = 0
    
    # Серия квестов (обновляется при завершении квеста)
    if pet.last_quest_completed_at and (now.date() - pet.last_quest_completed_at.date()).days > 1:
        pet.streaks["quest_completion"] = 0

def apply_user_action(pet: Pet, action: str, now: datetime) -> UserActionResult:
    """Применить действие, обновить квесты и вернуть результат."""
    result = _apply_base_action_effects(pet, action, now)
    if "Неизвестное действие" in result.message:
        return result
    
    # Обновление прогресса квеста
    if pet.daily_quests:
        for q_name, quest in pet.daily_quests.items():
            if not quest["completed"] and quest["action"] == action:
                quest["progress"] += 1
                _check_and_apply_quest_completion(pet, q_name, now)

    return result

def _check_and_apply_quest_completion(pet: Pet, quest_name: str, now: datetime):
    quest = pet.daily_quests.get(quest_name)
    if not quest or quest["completed"]:
        return

    if quest["progress"] >= quest["target"]:
        quest["completed"] = True
        # Применяем награду
        for stat, value in quest["reward"].items():
            current_val = getattr(pet, stat)
            setattr(pet, stat, clamp(current_val + value))
        
        # Обновляем серию
        if pet.last_quest_completed_at and (now.date() - pet.last_quest_completed_at.date()).days == 1:
            pet.streaks["quest_completion"] = pet.streaks.get("quest_completion", 0) + 1
        else:
            pet.streaks["quest_completion"] = 1
        pet.last_quest_completed_at = now

# ... (helper functions like _apply_base_action_effects, clamp, etc) ...

