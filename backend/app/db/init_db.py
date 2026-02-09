# backend/app/db/init_db.py — инициализация схемы БД (create_all) для MVP  # (я добавил)

from __future__ import annotations  # (я добавил)

from app.db.base import Base  # (я добавил)
from app.db.session import engine  # (я добавил)

# Важно: импорт моделей, чтобы они зарегистрировались в Base.metadata  # (я добавил)
from app.models import conversation as _conversation  # noqa: F401  # (я добавил)
from app.models import memory as _memory  # noqa: F401  # (я добавил)
from app.models import pet as _pet  # noqa: F401  # (я добавил)
from app.models import user as _user  # noqa: F401  # (я добавил)


async def init_db() -> None:
    """Создать таблицы в БД (MVP: без Alembic)."""  # (я добавил)
    async with engine.begin() as conn:  # (я добавил)
        await conn.run_sync(Base.metadata.create_all)  # (я добавил)
