# backend/app/schemas/auth.py — Pydantic схемы авторизации
# Назначение: схемы запросов/ответов auth

"""
Request/Response схемы для auth.
"""

from pydantic import BaseModel, EmailStr, field_validator


class RegisterIn(BaseModel):
    """Запрос регистрации."""
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        """Проверка пароля под bcrypt (лимит 72 байта)."""
        if len(value.encode("utf-8")) > 72:
            raise ValueError("Пароль слишком длинный (ограничение bcrypt — 72 байта).")  # (я добавил)
        if len(value) < 6:
            raise ValueError("Пароль слишком короткий (минимум 6 символов).")  # (я добавил)
        return value


class LoginIn(BaseModel):
    """Запрос логина."""
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        """Проверка пароля под bcrypt (лимит 72 байта)."""
        if len(value.encode("utf-8")) > 72:
            raise ValueError("Пароль слишком длинный (ограничение bcrypt — 72 байта).")  # (я добавил)
        return value


class TokenOut(BaseModel):
    """Ответ с access token."""
    access_token: str
    token_type: str = "bearer"


class MeOut(BaseModel):
    """Текущий пользователь."""
    id: str
    email: EmailStr
