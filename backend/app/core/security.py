# backend/app/core/security.py — безопасность (пароли, JWT)
"""
Хеширование паролей и работа с JWT access token.
"""

from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from passlib.context import CryptContext

from app.core.config import settings

_pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Вернуть bcrypt-хеш пароля."""
    return _pwd.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """Проверить пароль против хеша."""
    return _pwd.verify(password, password_hash)


def create_access_token(subject: str) -> str:
    """Создать JWT access token для subject (обычно user_id)."""
    now = datetime.now(timezone.utc)
    exp = now + timedelta(minutes=settings.access_token_ttl_minutes)
    payload: dict[str, Any] = {"sub": subject, "iat": int(now.timestamp()), "exp": int(exp.timestamp())}
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> dict[str, Any]:
    """Декодировать JWT, бросает исключение jwt при ошибке."""
    return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
