# backend/app/migrations/env.py — Alembic env
# Назначение: подключение Alembic к SQLAlchemy metadata и URL из Settings

from __future__ import annotations

from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.core.config import settings  # (я добавил)
from app.db.base import Base  # (я добавил)

# импорт моделей, чтобы Alembic видел таблицы  # (я добавил)
from app.models.user import User  # noqa: F401  # (я добавил)
from app.models.pet import Pet  # noqa: F401  # (я добавил)
from app.models.conversation import Conversation, Message  # noqa: F401  # (я добавил)
from app.models.memory import Memory  # noqa: F401  # (я добавил)

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata  # (я добавил)


def get_url() -> str:
    """URL базы данных для Alembic (sync driver)."""
    url = settings.database_url  # (я добавил)
    # Alembic работает синхронно, поэтому asyncpg надо заменить на psycopg  # (я добавил)
    return url.replace("postgresql+asyncpg://", "postgresql+psycopg://")  # (я добавил)



def run_migrations_offline() -> None:
    """Запуск миграций в offline режиме."""
    context.configure(
        url=get_url(),  # (я добавил)
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,  # (я добавил)
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Запуск миграций в online режиме."""
    connectable = engine_from_config(
        {"sqlalchemy.url": get_url()},  # (я добавил)
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        future=True,  # (я добавил)
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  # (я добавил)
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
