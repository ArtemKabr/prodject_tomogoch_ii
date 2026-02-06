# backend/app/api/pet.py — роуты питомца
"""
/pet/start, /pet, /pet/revive
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.pet import PetOut
from app.services.pet import get_pet_state, revive_pet, start_pet

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
