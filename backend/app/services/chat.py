# backend/app/services/chat.py — сервис чата
"""
Отправка сообщения, сохранение истории, генерация ответа, блокировка если питомец умер.
"""

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings  # (я добавил)
from app.models.conversation import Conversation, Message, MessageRole
from app.models.pet import Pet
from app.services.ollama_client import ollama_chat  # (я добавил)
from app.services.memory import (  # (я добавил)
    MemoryLimitExceeded,  # (я добавил)
    get_top_memories_texts,
    upsert_memory_from_chat,  # (я добавил)
)
from app.services.pet_rules import apply_action_from_user_message, apply_passive_degradation


async def _get_or_create_conversation(  # (я добавил)
    db: AsyncSession,  # (я добавил)
    user_id: str,  # (я добавил)
    pet_id: int,  # (я добавил)
    conversation_id: int | None,  # (я добавил)
) -> Conversation:  # (я добавил)
    if conversation_id is not None:
        conv = (await db.execute(
            select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id,
                Conversation.pet_id == pet_id,  # (я добавил)
            )
        )).scalar_one_or_none()
        if conv is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
        return conv

    conv = Conversation(user_id=user_id, pet_id=pet_id)
    db.add(conv)
    await db.flush()
    return conv


async def send_message(
    db: AsyncSession,
    *,
    user_id: str,
    pet: Pet,
    conversation_id: int | None,
    user_text: str,
) -> tuple[str, Pet, str, int]:
    """Отправить сообщение в чат и вернуть (assistant_text, pet, stage, conversation_id)."""
    apply_passive_degradation(pet)  # (я добавил)
    if not pet.is_alive:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Pet is dead")

    conv = await _get_or_create_conversation(db, user_id, pet.id, conversation_id)

    # сохраняем сообщение пользователя  # (я добавил)
    db.add(Message(conversation_id=conv.id, role=MessageRole.user.value, text=user_text))  # (я добавил)

    normalized = (user_text or "").strip()  # (я добавил)
    low = normalized.lower()  # (я добавил)

    if not normalized:  # (я добавил)
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Empty message")  # (я добавил)

    if settings.auto_memory_enabled:  # (я добавил)
        # === автосохранение памяти из обычной речи (без команды) ===  # (я добавил)
        if not (low.startswith("запомни:") or low.startswith("запомни ")):  # (я добавил)
            # from app.models.memory import Memory  # (старое оставил)  # (я добавил)

            preference_prefixes = (  # (я добавил)
                "я люблю",  # (я добавил)
                "мне нравится",  # (я добавил)
                "я предпочитаю",  # (я добавил)
                "я хочу",  # (я добавил)
                "я не люблю",  # (я добавил)
                "мне не нравится",  # (я добавил)
                "я ненавижу",  # (я добавил)
            )
            profile_prefixes = (  # (я добавил)
                "меня зовут",  # (я добавил)
                "я работаю",  # (я добавил)
                "я живу",  # (я добавил)
                "мой возраст",  # (я добавил)
                "я программист",  # (я добавил)
                "я разработчик",  # (я добавил)
            )

            mem_type: str | None = None  # (я добавил)
            importance = 4  # (я добавил)

            if low.startswith(preference_prefixes):  # (я добавил)
                mem_type = "preference"  # (я добавил)
                importance = 5  # (я добавил)
            elif low.startswith(profile_prefixes):  # (я добавил)
                mem_type = "profile"  # (я добавил)

            if mem_type is not None:  # (я добавил)
                payload_text = normalized[:200].strip()  # (я добавил)
                payload_text_clean = " ".join(payload_text.split()).strip()  # (я добавил)

                # exists_mem = (await db.execute(  # (старое оставил)  # (я добавил)
                #     select(Memory.id).where(
                #         Memory.user_id == user_id,
                #         Memory.type == mem_type,
                #         func.lower(Memory.text) == payload_text_clean.lower(),
                #     )
                # )).scalar_one_or_none()

                # if exists_mem is None:
                #     db.add(Memory(...))
                #     await db.flush()

                try:  # (я добавил)
                    await upsert_memory_from_chat(  # (я добавил)
                        db,
                        user_id=user_id,
                        type_=mem_type,
                        text=payload_text_clean,
                        importance=importance,
                    )
                except MemoryLimitExceeded:  # (я добавил)
                    pass  # (я добавил)

        # === автосохранение памяти по триггеру "запомни" ===  # (я добавил)
        if low.startswith("запомни:") or low.startswith("запомни "):  # (я добавил)
            # from app.models.memory import Memory  # (старое оставил)  # (я добавил)

            payload_text = (  # (я добавил)
                normalized.split(":", 1)[1].strip()
                if ":" in normalized
                else normalized[7:].strip()
            )

            if payload_text:  # (я добавил)
                payload_low = payload_text.lower().strip()  # (я добавил)

                preference_prefixes = (  # (я добавил)
                    "я люблю",  # (я добавил)
                    "мне нравится",  # (я добавил)
                    "я предпочитаю",  # (я добавил)
                    "я хочу",  # (я добавил)
                    "я не люблю",  # (я добавил)
                    "мне не нравится",  # (я добавил)
                    "я ненавижу",  # (я добавил)
                )
                profile_prefixes = (  # (я добавил)
                    "меня зовут",  # (я добавил)
                    "я работаю",  # (я добавил)
                    "я живу",  # (я добавил)
                    "мне ",  # (я добавил)
                    "мой возраст",  # (я добавил)
                    "я программист",  # (я добавил)
                    "я разработчик",  # (я добавил)
                )

                mem_type = "profile"  # (я добавил)
                importance = 4  # (я добавил)
                if payload_low.startswith(preference_prefixes):  # (я добавил)
                    mem_type = "preference"  # (я добавил)
                    importance = 5  # (я добавил)
                elif payload_low.startswith(profile_prefixes):  # (я добавил)
                    mem_type = "profile"  # (я добавил)

                payload_text_clean = " ".join(payload_text.split()).strip()  # (я добавил)

                # exists_mem = (await db.execute(  # (старое оставил)  # (я добавил)
                #     select(Memory.id).where(
                #         Memory.user_id == user_id,
                #         Memory.type == mem_type,
                #         func.lower(Memory.text) == payload_text_clean.lower(),
                #     )
                # )).scalar_one_or_none()
                #
                # if exists_mem is None:
                #     db.add(Memory(...))
                #     await db.flush()

                try:  # (я добавил)
                    await upsert_memory_from_chat(  # (я добавил)
                        db,
                        user_id=user_id,
                        type_=mem_type,
                        text=payload_text_clean[:200],
                        importance=importance,
                    )
                except MemoryLimitExceeded:  # (я добавил)
                    pass  # (я добавил)

    # применяем влияние действия пользователя на питомца  # (я добавил)
    apply_action_from_user_message(pet, user_text=user_text)  # (я добавил)

    # получаем актуальную память (уже с учётом возможного добавления)  # (я добавил)
    mem_texts = await get_top_memories_texts(db, user_id, limit=10)

    system = (  # (я добавил)
        "Ты — ИИ-питомец (тамагочи). "
        "Отвечай по-русски, дружелюбно, кратко (1–5 предложений). "
        "Если говоришь 'я помню' — опирайся ТОЛЬКО на блок 'Контекст (память о пользователе)'. "  # (я добавил)
        "Не добавляй в память и не утверждай факты о пользователе, которых нет в этом блоке. "  # (я добавил)
        "Не выдумывай факты про погоду/дату/время/новости без источников. "
        "Если не знаешь — так и скажи."
    )

    memory_block = "\n".join(f"- {t}" for t in mem_texts)  # (я добавил)
    prompt = (  # (я добавил)
        "Контекст (память о пользователе):\n"
        f"{memory_block if memory_block else '(нет)'}\n\n"
        f"Состояние питомца: age_stage={pet.age_stage}, health={pet.health}, "
        f"energy={pet.energy}, mood={pet.mood}, intellect={pet.intellect}, bond={pet.bond}\n\n"
        f"Сообщение пользователя: {user_text}\n"
    )

    assistant_text = await ollama_chat(prompt=prompt, system=system)  # (я добавил)

    # сохраняем ответ ассистента  # (я добавил)
    db.add(Message(conversation_id=conv.id, role=MessageRole.assistant.value, text=assistant_text))  # (я добавил)

    await db.commit()
    await db.refresh(pet)

    return assistant_text, pet, pet.age_stage, conv.id
