# backend/app/api/ai.py — API-ручки для общения с ИИ  # (я добавил)

from __future__ import annotations  # (я добавил)

from pydantic import BaseModel  # (я добавил)
from fastapi import APIRouter, HTTPException  # (я добавил)

from app.services.ollama_client import ollama_chat  # (я добавил)

router = APIRouter(prefix="/api/ai", tags=["ai"])  # (я добавил)


class ChatIn(BaseModel):
    message: str


class ChatOut(BaseModel):
    answer: str


@router.post("/chat", response_model=ChatOut)
async def chat(body: ChatIn) -> ChatOut:
    """Чат с моделью через Ollama."""
    msg = body.message.strip()
    if not msg:
        raise HTTPException(status_code=400, detail="Пустое сообщение")

    system = (
        "Ты — дружелюбный ИИ-питомец в стиле тамагочи. "
        "Отвечай кратко, по-русски, без токсичности. "
        "Если пользователь спрашивает что ты умеешь — перечисли 5-7 возможностей."
    )

    answer = await ollama_chat(prompt=msg, system=system)
    return ChatOut(answer=answer)
