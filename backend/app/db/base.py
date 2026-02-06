# backend/app/db/base.py — базовый класс моделей
"""
Declarative Base для SQLAlchemy моделей.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Базовый класс для всех моделей."""
