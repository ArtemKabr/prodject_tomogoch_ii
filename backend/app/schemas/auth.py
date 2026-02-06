# backend/app/schemas/auth.py — Pydantic схемы авторизации
"""
Request/Response схемы для auth.
"""

from pydantic import BaseModel, EmailStr


class RegisterIn(BaseModel):
    """Запрос регистрации."""
    email: EmailStr
    password: str


class LoginIn(BaseModel):
    """Запрос логина."""
    email: EmailStr
    password: str


class TokenOut(BaseModel):
    """Ответ с access token."""
    access_token: str
    token_type: str = "bearer"


class MeOut(BaseModel):
    """Текущий пользователь."""
    id: str
    email: EmailStr
