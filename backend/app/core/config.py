# backend/app/core/config.py — конфиг и переменные окружения
"""
Настройки приложения (env -> Pydantic Settings).
"""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки приложения из переменных окружения."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "ai-tamagotchi"  # (я добавил)
    env: str = "local"  # (я добавил)

    database_url: str = Field(..., alias="DATABASE_URL")  # (я добавил)

    jwt_secret: str = Field(..., alias="JWT_SECRET")  # (я добавил)
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")  # (я добавил)
    access_token_ttl_minutes: int = Field(
        default=60 * 24,
        alias="ACCESS_TOKEN_TTL_MINUTES",
    )  # (я добавил)

    # === Ollama ===
    ollama_base_url: str = Field(  # (я добавил)
        default="http://127.0.0.1:11434",
        alias="OLLAMA_BASE_URL",
    )
    ollama_model: str = Field(  # (я добавил)
        default="llama31-local",
        alias="OLLAMA_MODEL",
    )
    ollama_timeout_s: float = Field(  # (я добавил)
        default=120.0,
        alias="OLLAMA_TIMEOUT_S",
    )

    auto_memory_enabled: bool = Field(  # (я добавил)
        default=True,
        alias="AUTO_MEMORY_ENABLED",
    )

    # === Rate limit (chat) ===  # (я добавил)
    rate_limit_enabled: bool = Field(  # (я добавил)
        default=True,
        alias="RATE_LIMIT_ENABLED",
    )  # (я добавил)

    rate_limit_requests: int = Field(  # (я добавил)
        default=20,
        alias="RATE_LIMIT_REQUESTS",
    )  # (я добавил)

    rate_limit_window_s: int = Field(  # (я добавил)
        default=60,
        alias="RATE_LIMIT_WINDOW_S",
    )  # (я добавил)


settings = Settings()
