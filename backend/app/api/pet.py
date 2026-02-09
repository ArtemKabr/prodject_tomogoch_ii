# backend/app/api/pet.py

from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.pet import PetOut
from app.schemas.pet_action import PetActionIn, PetActionOut, PetStatusOut
from app.services import pet as pet_service
from app.services import pet_rules

router = APIRouter(prefix="/api/v1/pet", tags=["pet"])


@router.post("/action", response_model=PetActionOut)
async def perform_action(
    payload: PetActionIn,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> PetActionOut:
    now = datetime.now(timezone.utc)
    pet = await pet_service.get_pet_for_update(db, user_id=user.id)
    if not pet:
        raise HTTPException(status_code=404, detail="Питомец не найден.")

    pet_rules.apply_debts_and_degradation(pet, user.timezone, now)
    
    available_actions = pet_rules.get_available_actions(pet, now, user.timezone)
    if payload.action not in available_actions:
        raise HTTPException(status_code=400, detail="Действие сейчас недоступно.")

    result = pet_rules.apply_user_action(pet, payload.action, now)

    await db.commit()
    await db.refresh(pet)

    return PetActionOut(
        message=result.message,
        pet_state=PetOut.model_validate(pet, from_attributes=True).model_dump(),
    )


@router.get("/status", response_model=PetStatusOut)
async def get_status(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> PetStatusOut:
    now = datetime.now(timezone.utc)
    pet = await pet_service.get_pet_state(db, user_id=user.id)
    if not pet:
        raise HTTPException(status_code=404, detail="Питомец не найден.")

    # Фаза 5: Обновление игровой логики
    pet_rules.determine_personality(pet)
    pet_rules.generate_daily_quests(pet, now, user.timezone)
    pet_rules.update_streaks(pet, now)

    pet_rules.apply_debts_and_degradation(pet, user.timezone, now)

    needs = []
    if pet.hunger_debt > 50: needs.append("feed")
    if pet.sleep_debt > 50: needs.append("sleep")
    if pet.mood < 30: needs.append("play")

    available_actions = pet_rules.get_available_actions(pet, now, user.timezone)
    cooldowns = {a: pet_rules.ACTION_COOLDOWNS_SECONDS.get(a, 0) for a in pet_rules.ACTION_COOLDOWNS_SECONDS}

    # Расширяем PetStatusOut новыми данными
    return PetStatusOut(
        time_of_day=pet_rules.get_time_of_day(now, user.timezone),
        needs=needs,
        available_actions=available_actions,
        cooldowns=cooldowns,
        daily_quests=pet.daily_quests,
        streaks=pet.streaks,
        personality=pet.personality_type,
        pet_state=PetOut.model_validate(pet, from_attributes=True).model_dump(),
    )

# ... (остальные эндпоинты) ...
