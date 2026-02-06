# backend/app/services/memory.py — сервис памяти
"""
CRUD памяти пользователя + выбор актуальных записей для ответа.
"""

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.memory import Memory


async def list_memories(db: AsyncSession, user_id: str) -> list[Memory]:
    """Вернуть все записи памяти пользователя (сортировка по importance/updated_at)."""
    stmt = (
        select(Memory)
        .where(Memory.user_id == user_id)
        .order_by(Memory.importance.desc(), Memory.updated_at.desc().nullslast(), Memory.created_at.desc())
    )
    return list((await db.execute(stmt)).scalars().all())


async def get_top_memories_texts(db: AsyncSession, user_id: str, limit: int = 10) -> list[str]:
    """Вернуть тексты топ-N записей памяти для подмешивания в ответ."""
    stmt = (
        select(Memory.text)
        .where(Memory.user_id == user_id)
        .order_by(Memory.importance.desc(), Memory.updated_at.desc().nullslast(), Memory.created_at.desc())
        .limit(limit)
    )
    rows = (await db.execute(stmt)).all()
    return [r[0] for r in rows]


async def add_memory(db: AsyncSession, mem: Memory) -> Memory:
    """Добавить запись памяти."""
    db.add(mem)
    await db.commit()
    await db.refresh(mem)
    return mem


async def delete_memory(db: AsyncSession, user_id: str, memory_id: int) -> None:
    """Удалить запись памяти пользователя по id."""
    await db.execute(delete(Memory).where(Memory.id == memory_id, Memory.user_id == user_id))
    await db.commit()
