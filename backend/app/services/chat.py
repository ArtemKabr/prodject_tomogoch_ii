# backend/app/services/chat.py — сервис чата
"""
Отправка сообщения, сохранение истории, генерация ответа, блокировка если питомец умер.
"""

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.conversation import Conversation, Message, MessageRole
from app.models.pet import Pet
from app.providers.llm import generate_reply
from app.services.memory import get_top_memories_texts
from app.services.pet_rules import apply_action_from_user_message, apply_passive_degradation


async def _get_or_create_conversation(db: AsyncSession, user_id: str, pet_id: int, conversation_id: int | None) -> Conversation:
    if conversation_id is not None:
        conv = (await db.execute(
            select(Conversation).where(Conversation.id == conversation_id, Conversation.user_id == user_id)
        )).scalar_one_or_none()
        if conv is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
        return conv

    conv = Conversation(user_id=user_id, pet_id=pet_id)  # (я добавил)
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

    db.add(Message(conversation_id=conv.id, role=MessageRole.user.value, text=user_text))  # (я добавил)

    apply_action_from_user_message(pet)  # (я добавил)

    mem_texts = await get_top_memories_texts(db, user_id, limit=10)
    reply = generate_reply(pet=pet, user_message=user_text, memory_texts=mem_texts)

    db.add(Message(conversation_id=conv.id, role=MessageRole.assistant.value, text=reply.text))  # (я добавил)

    await db.commit()
    await db.refresh(pet)

    return reply.text, pet, pet.age_stage, conv.id
