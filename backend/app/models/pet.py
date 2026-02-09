# backend/app/models/pet.py

from datetime import datetime
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base

class Pet(Base):
    __tablename__ = "pet"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))

    name: Mapped[str] = mapped_column(String, default="Petya")
    age_stage: Mapped[str] = mapped_column(String, default="egg")
    is_alive: Mapped[bool] = mapped_column(default=True)

    health: Mapped[float] = mapped_column(Float, default=100.0)
    energy: Mapped[float] = mapped_column(Float, default=100.0)
    mood: Mapped[float] = mapped_column(Float, default=100.0)
    intellect: Mapped[float] = mapped_column(Float, default=0.0)
    bond: Mapped[float] = mapped_column(Float, default=0.0)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_active_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Фаза 1
    last_feed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_walk_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_play_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_train_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_sleep_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_action_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    sleep_debt: Mapped[float] = mapped_column(Float, default=0.0)
    hunger_debt: Mapped[float] = mapped_column(Float, default=0.0)
    
    # Фаза 5
    personality_type: Mapped[str] = mapped_column(String, nullable=True) # e.g., "intellectual", "active"
    daily_quests: Mapped[dict] = mapped_column(JSON, default=lambda: {})
    streaks: Mapped[dict] = mapped_column(JSON, default=lambda: {"login": 0, "quest_completion": 0})
    last_quest_completed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
