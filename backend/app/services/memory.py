# backend/app/services/memory.py — сервис памяти
"""
CRUD памяти пользователя + выбор актуальных записей для ответа.
"""

from __future__ import annotations  # (я добавил)

import re  # (я добавил)

from sqlalchemy import delete, select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.memory import Memory


# === настройки ===
_MEMORY_LIMIT_PER_USER = 200  # (я добавил)
_RX_SPACES = re.compile(r"\s+")  # (я добавил)


class MemoryLimitExceeded(Exception):  # (я добавил)
    """Превышен лимит записей памяти пользователя."""  # (я добавил)


def _normalize_text(text: str) -> str:  # (я добавил)
    """Нормализовать текст памяти: trim + lower + collapse spaces."""  # (я добавил)
    return _RX_SPACES.sub(" ", text.strip()).lower()  # (я добавил)


async def list_memories(db: AsyncSession, user_id: str) -> list[Memory]:
    """Вернуть все записи памяти пользователя (сортировка по importance/updated_at)."""
    stmt = (
        select(Memory)
        .where(Memory.user_id == user_id)
        .order_by(
            Memory.importance.desc(),
            Memory.updated_at.desc().nullslast(),
            Memory.created_at.desc(),
        )
    )
    return list((await db.execute(stmt)).scalars().all())


async def get_top_memories_texts(db: AsyncSession, user_id: str, limit: int = 10) -> list[str]:
    """Вернуть тексты топ-N записей памяти для подмешивания в ответ."""
    stmt = (
        select(Memory.text)
        .where(Memory.user_id == user_id)
        .order_by(
            Memory.importance.desc(),
            Memory.updated_at.desc().nullslast(),
            Memory.created_at.desc(),
        )
        .limit(limit)
    )
    rows = (await db.execute(stmt)).all()
    return [r[0] for r in rows]


async def _count_user_memories(db: AsyncSession, user_id: str) -> int:  # (я добавил)
    """Количество записей памяти пользователя."""  # (я добавил)
    stmt = select(func.count()).select_from(Memory).where(Memory.user_id == user_id)  # (я добавил)
    return int((await db.execute(stmt)).scalar_one())  # (я добавил)


async def add_memory(db: AsyncSession, mem: Memory) -> Memory:
    """
    Добавить запись памяти:
    - нормализация текста
    - дедуп по lower(trim(text))
    - лимит на пользователя
    """
    text_clean = _RX_SPACES.sub(" ", (mem.text or "").strip())  # (я добавил)
    if not text_clean:
        return mem

    text_norm = _normalize_text(text_clean)  # (я добавил)

    # дедуп  # (я добавил)
    exists = (await db.execute(
        select(Memory).where(
            Memory.user_id == mem.user_id,
            func.lower(func.trim(Memory.text)) == text_norm,
        )
    )).scalar_one_or_none()

    if exists is not None:
        # усилим важность, если новая выше  # (я добавил)
        exists.importance = max(exists.importance, mem.importance)  # (я добавил)
        await db.commit()  # (я добавил)
        await db.refresh(exists)  # (я добавил)
        return exists  # (я добавил)

    # лимит  # (я добавил)
    total = await _count_user_memories(db, mem.user_id)  # (я добавил)
    if total >= _MEMORY_LIMIT_PER_USER:  # (я добавил)
        raise MemoryLimitExceeded()  # (я добавил)

    mem.text = text_clean  # (я добавил)
    db.add(mem)

    try:
        await db.commit()
        await db.refresh(mem)
        return mem
    except IntegrityError:
        await db.rollback()
        # гонка — вернём существующую  # (я добавил)
        exists_after = (await db.execute(
            select(Memory).where(
                Memory.user_id == mem.user_id,
                func.lower(func.trim(Memory.text)) == text_norm,
            )
        )).scalar_one()
        return exists_after  # (я добавил)


async def upsert_memory_from_chat(  # (я добавил)
    db: AsyncSession,
    *,
    user_id: str,
    type_: str,
    text: str,
    importance: int = 3,
) -> Memory:
    """Upsert памяти из чата (используется chat-сервисом)."""  # (я добавил)
    mem = Memory(
        user_id=user_id,
        type=type_,
        text=text,
        importance=importance,
    )
    return await add_memory(db, mem)


async def delete_memory(db: AsyncSession, user_id: str, memory_id: int) -> None:
    """Удалить запись памяти пользователя по id."""
    await db.execute(
        delete(Memory).where(
            Memory.id == memory_id,
            Memory.user_id == user_id,
        )
    )
    await db.commit()
