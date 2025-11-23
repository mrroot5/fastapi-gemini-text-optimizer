"""Application configuration using Pydantic Settings."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Gemini AI Configuration
    gemini_api_key: str = ""
    gemini_model: str = ""
    gemini_temperature: float = 0.0
    gemini_max_tokens: int = 0

    # Application Configuration
    environment: str = ""
    debug: bool = True

    # Authentication Tokens (for demo purposes)
    query_token: str = ""
    header_token: str = ""


# Global settings instance
@lru_cache
def get_settings() -> Settings:
    return Settings()
