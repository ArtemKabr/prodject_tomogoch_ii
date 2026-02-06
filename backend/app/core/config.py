# backend/app/core/config.py — конфиг и переменные окружения
"""
Настройки приложения (env -> Pydantic Settings).
"""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки приложения из переменных окружения."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "ai-tamagotchi"  # (я добавил)
    env: str = "local"  # (я добавил)

    database_url: str = Field(..., alias="DATABASE_URL")  # (я добавил)

    jwt_secret: str = Field(..., alias="JWT_SECRET")  # (я добавил)
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")  # (я добавил)
    access_token_ttl_minutes: int = Field(default=60 * 24, alias="ACCESS_TOKEN_TTL_MINUTES")  # (я добавил)


settings = Settings()
