# backend/app/main.py — точка входа FastAPI
"""
Подключение роутеров и запуск приложения.
"""

from fastapi import FastAPI

from app.api.ai import router as ai_router
from app.api.auth import router as auth_router
from app.api.chat import router as chat_router
from app.api.memory import router as memory_router
from app.api.pet import router as pet_router
from app.core.config import settings
from app.db.init_db import init_db  # (я добавил)

app = FastAPI(title=settings.app_name)


@app.on_event("startup")
async def _startup() -> None:
    """Инициализация схемы БД для MVP (create_all)."""  # (я добавил)
    await init_db()  # (я добавил)


app.include_router(auth_router)
app.include_router(pet_router)
app.include_router(chat_router)
app.include_router(memory_router)
app.include_router(ai_router)
