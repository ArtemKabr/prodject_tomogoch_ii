# backend/app/providers/llm.py — провайдер генерации ответа (заглушка MVP)
"""
LLM provider для MVP: шаблонные ответы по стадии/настроению/энергии и памяти.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.models.pet import Pet


@dataclass(frozen=True)
class LLMReply:
    """Ответ провайдера."""

    text: str


def _tone(mood: int) -> str:
    if mood >= 70:
        return "радостно"
    if mood >= 40:
        return "спокойно"
    return "ворчливо"


def _length_hint(energy: int) -> str:
    if energy >= 70:
        return "длинно"
    if energy >= 40:
        return "средне"
    return "коротко"


def generate_reply(*, pet: Pet, user_message: str, memory_texts: list[str]) -> LLMReply:
    """Сгенерировать ответ (MVP заглушка)."""
    tone = _tone(pet.mood)
    length = _length_hint(pet.energy)

    memory_block = ""
    if memory_texts:
        # максимум 10 записей уже обеспечиваем на уровне сервиса  # (я добавил)
        memory_block = " Я помню: " + "; ".join(memory_texts)

    text = (
        f"[{pet.age_stage}] ({tone}, {length}) "
        f"Ты сказал: «{user_message}».{memory_block}"
    )
    return LLMReply(text=text)
