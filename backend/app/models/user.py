# backend/app/models/user.py — модель пользователя
"""
Users: регистрация/авторизация.
"""

from datetime import datetime, timezone

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class User(Base):
    """Пользователь приложения."""

    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True)  # (я добавил) uuid хранить строкой на MVP
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    pets = relationship("Pet", back_populates="user")  # (я добавил)
