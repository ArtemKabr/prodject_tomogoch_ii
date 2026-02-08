# backend/app/api/pet.py — роуты питомца
"""
/pet/start, /pet, /pet/revive, /pet/action, /pet/status
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.pet import PetOut
from app.schemas.pet_action import PetActionIn, PetActionOut, PetStatusOut  # (я добавил)
from app.services.pet import (
    get_pet_state,
    revive_pet,
    start_pet,
    perform_pet_action,  # (я добавил)
)
from app.services.pet_rules import get_time_of_day, get_available_actions  # (я добавил)

router = APIRouter(prefix="/api/v1/pet", tags=["pet"])


@router.post("/start", response_model=PetOut)
async def start(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> PetOut:
    pet = await start_pet(db, user.id)
    return PetOut.model_validate(pet, from_attributes=True)


@router.get("", response_model=PetOut)
async def get_state(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> PetOut:
    pet = await get_pet_state(db, user.id)
    return PetOut.model_validate(pet, from_attributes=True)


@router.post("/revive", response_model=PetOut)
async def revive(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> PetOut:
    pet = await revive_pet(db, user.id)
    return PetOut.model_validate(pet, from_attributes=True)


@router.post("/action", response_model=PetActionOut)  # (я добавил)
async def action(  # (я добавил)
    payload: PetActionIn,  # (я добавил)
    user: User = Depends(get_current_user),  # (я добавил)
    db: AsyncSession = Depends(get_db),  # (я добавил)
) -> PetActionOut:  # (я добавил)
    pet, message, _tod, _available = await perform_pet_action(  # (я добавил)
        db,
        user_id=user.id,
        action=payload.action,
    )

    return PetActionOut(  # (я добавил)
        message=message,  # (я добавил)
        pet_state=PetOut.model_validate(pet, from_attributes=True).model_dump(),  # (я добавил)
    )


@router.get("/status", response_model=PetStatusOut)  # (я добавил)
async def status(  # (я добавил)
    user: User = Depends(get_current_user),  # (я добавил)
    db: AsyncSession = Depends(get_db),  # (я добавил)
) -> PetStatusOut:  # (я добавил)
    pet = await get_pet_state(db, user.id)  # (я добавил)

    now = pet.last_active_at  # (я добавил)
    time_of_day = get_time_of_day(now)  # (я добавил)
    available_actions = get_available_actions(pet=pet, now=now)  # (я добавил)

    needs: list[str] = []  # (я добавил)
    if pet.health <= 30:  # (я добавил)
        needs.append("heal")  # (я добавил)
    if pet.energy <= 30:  # (я добавил)
        needs.append("feed")  # (я добавил)
    if pet.energy <= 20 and time_of_day == "night":  # (я добавил)
        needs.append("sleep")  # (я добавил)
    if pet.mood <= 30:  # (я добавил)
        needs.append("play")  # (я добавил)

    return PetStatusOut(  # (я добавил)
        time_of_day=time_of_day,  # (я добавил)
        needs=needs,  # (я добавил)
        available_actions=available_actions,  # (я добавил)
        pet_state=PetOut.model_validate(pet, from_attributes=True).model_dump(),  # (я добавил)
    )
