# backend/app/services/ollama_client.py — клиент для Ollama API  # (я добавил)

from __future__ import annotations  # (я добавил)

from typing import Any  # (я добавил)

import httpx  # (я добавил)

from app.core.config import settings  # (я добавил)


async def ollama_chat(prompt: str, system: str | None = None) -> str:
    """Отправляет промпт в Ollama и возвращает итоговый текст ответа."""  # (я добавил)
    payload: dict[str, Any] = {
        "model": settings.ollama_model,
        "prompt": prompt,
        "stream": False,
    }
    if system:
        payload["system"] = system

    async with httpx.AsyncClient(timeout=settings.ollama_timeout_s) as client:
        r = await client.post(f"{settings.ollama_base_url}/api/generate", json=payload)
        r.raise_for_status()
        data = r.json()

    return (data.get("response") or "").strip()
