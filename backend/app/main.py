# backend/app/main.py — точка входа FastAPI
"""
Подключение роутеров и запуск приложения.
"""

from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.chat import router as chat_router
from app.api.memory import router as memory_router
from app.api.pet import router as pet_router
from app.core.config import settings

app = FastAPI(title=settings.app_name)

app.include_router(auth_router)
app.include_router(pet_router)
app.include_router(chat_router)
app.include_router(memory_router)
