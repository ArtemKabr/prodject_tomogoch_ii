# backend/app/db/session.py — подключение к БД и фабрика сессий
"""
SQLAlchemy engine + async session maker.
"""

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings

engine = create_async_engine(settings.database_url, pool_pre_ping=True)  # (я добавил)
async_session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(  # (я добавил)
    bind=engine,
    expire_on_commit=False,
)
