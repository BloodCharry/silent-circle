from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    APP_NAME: str = "Silent Circle"
    API_V1_PREFIX: str = "/api/v1"
    TELEGRAM_BOT_TOKEN: str

    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://user:password@localhost:5432/silentcircle",
        description="PostgreSQL DSN"
    )
    REDIS_URL: str = Field(
        default="redis://localhost:6379/0",
        description="Redis DSN"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()  # type: ignore[call-arg]
