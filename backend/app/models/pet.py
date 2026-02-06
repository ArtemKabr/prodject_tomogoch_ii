# backend/app/models/pet.py — модель питомца
"""
Pets: параметры 0..100, стадия, жизнь/смерть.
"""

from datetime import datetime
from enum import StrEnum

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class AgeStage(StrEnum):
    """Стадии развития питомца."""

    baby = "baby"
    teen = "teen"
    adult = "adult"
    mentor = "mentor"


class Pet(Base):
    """Питомец пользователя (активный/архив)."""

    __tablename__ = "pets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), index=True, nullable=False)

    age_stage: Mapped[str] = mapped_column(String(16), default=AgeStage.baby.value, nullable=False)

    health: Mapped[int] = mapped_column(Integer, default=100, nullable=False)
    energy: Mapped[int] = mapped_column(Integer, default=80, nullable=False)
    mood: Mapped[int] = mapped_column(Integer, default=60, nullable=False)
    intellect: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    bond: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    is_alive: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    last_active_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    died_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="pets")  # (я добавил)
    conversations = relationship("Conversation", back_populates="pet")  # (я добавил)
