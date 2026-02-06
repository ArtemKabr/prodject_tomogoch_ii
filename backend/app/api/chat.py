# backend/app/api/chat.py — роуты чата
"""
/chat, /chat/history
"""

from fastapi import APIRouter, Depends, HTTPException, status  # (я добавил)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user, get_db
from app.models.conversation import Message
from app.models.user import User
from app.schemas.chat import ChatIn, ChatOut
from app.schemas.pet import PetOut
from app.services.chat import send_message
from app.services.pet import get_alive_pet

router = APIRouter(prefix="/api/v1/chat", tags=["chat"])


@router.post("", response_model=ChatOut)
async def chat(payload: ChatIn, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> ChatOut:
    pet = await get_alive_pet(db, user.id)
    if pet is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found")  # (я добавил)

    assistant_text, pet, stage, conv_id = await send_message(
        db,
        user_id=user.id,
        pet=pet,
        conversation_id=payload.conversation_id,
        user_text=payload.message,
    )

    return ChatOut(
        assistant_message=assistant_text,
        stage=stage,
        conversation_id=conv_id,
        pet_state=PetOut.model_validate(pet, from_attributes=True).model_dump(),
    )


@router.get("/history")
async def history(
    conversation_id: int,
    limit: int = 20,
    offset: int = 0,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    stmt = (
        select(Message)
        .join(Message.conversation)
        .where(Message.conversation_id == conversation_id)
        .limit(limit)
        .offset(offset)
        .order_by(Message.created_at.asc())
    )
    rows = (await db.execute(stmt)).scalars().all()
    return {"items": [{"role": m.role, "text": m.text, "created_at": m.created_at} for m in rows]}
