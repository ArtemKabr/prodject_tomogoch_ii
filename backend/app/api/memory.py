# backend/app/api/memory.py — роуты памяти
"""
/memory list/add/delete
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user, get_db
from app.models.memory import Memory
from app.models.user import User
from app.schemas.memory import MemoryIn, MemoryOut
from app.services.memory import add_memory, delete_memory, list_memories

router = APIRouter(prefix="/api/v1/memory", tags=["memory"])


@router.get("", response_model=list[MemoryOut])
async def get_all(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> list[MemoryOut]:
    items = await list_memories(db, user.id)
    return [MemoryOut.model_validate(x, from_attributes=True) for x in items]


@router.post("", response_model=MemoryOut, status_code=201)
async def add(payload: MemoryIn, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> MemoryOut:
    mem = Memory(user_id=user.id, type=payload.type, text=payload.text, importance=payload.importance)
    mem = await add_memory(db, mem)
    return MemoryOut.model_validate(mem, from_attributes=True)


@router.delete("/{memory_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(memory_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> None:
    await delete_memory(db, user.id, memory_id)
    return None
