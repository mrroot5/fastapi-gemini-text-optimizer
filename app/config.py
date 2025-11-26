"""Application configuration using Pydantic Settings."""

import logging
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
    # Logging
    log_level: str = ""

    # Authentication Tokens
    query_token: str = ""
    header_token: str = ""


@lru_cache
def get_settings() -> Settings:
    settings = Settings()

    _configure_root_logging(settings)

    return settings


def _configure_root_logging(settings: Settings) -> None:
    try:
        level = getattr(logging, settings.log_level.upper(), logging.INFO)
    except Exception:
        level = logging.INFO

    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    logging.getLogger().setLevel(level)

    return None
