# backend/app/services/pet.py — сервис питомца
"""
Создание питомца, получение состояния, revive, проверка жив/мертв.
"""

from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.pet import Pet
from app.services.pet_rules import apply_passive_degradation


async def get_alive_pet(db: AsyncSession, user_id: str) -> Pet | None:
    """Получить живого питомца пользователя."""
    stmt = select(Pet).where(and_(Pet.user_id == user_id, Pet.is_alive.is_(True)))
    return (await db.execute(stmt)).scalar_one_or_none()


async def start_pet(db: AsyncSession, user_id: str) -> Pet:
    """Создать питомца, если живого нет."""
    alive = await get_alive_pet(db, user_id)
    if alive is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Pet already exists")

    pet = Pet(user_id=user_id, last_active_at=datetime.now(timezone.utc))  # (я добавил)
    db.add(pet)
    await db.commit()
    await db.refresh(pet)
    return pet


async def get_pet_state(db: AsyncSession, user_id: str) -> Pet:
    """Получить состояние питомца (живого или последнего), с деградацией."""
    pet = await get_alive_pet(db, user_id)
    if pet is None:
        # если живого нет — отдаём 404 (на фронте будет кнопка start/revive)  # (я добавил)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found")

    apply_passive_degradation(pet)  # (я добавил)
    await db.commit()
    await db.refresh(pet)
    return pet


async def revive_pet(db: AsyncSession, user_id: str) -> Pet:
    """Создать нового питомца после смерти (MVP: просто новый, старых не трогаем)."""
    alive = await get_alive_pet(db, user_id)
    if alive is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Pet already alive")

    pet = Pet(user_id=user_id, last_active_at=datetime.now(timezone.utc))  # (я добавил)
    db.add(pet)
    await db.commit()
    await db.refresh(pet)
    return pet
