"""Application configuration using Pydantic Settings."""

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
    gemini_api_key: str = "AIzaSyBH3Qa5fauhNcAUWGm4sCi9h9vdUN88-sI"
    gemini_model: str = "gemini-2.0-flash-exp"
    gemini_temperature: float = 0.7
    gemini_max_tokens: int = 2048

    # Application Configuration
    environment: str = "development"
    debug: bool = True

    # Authentication Tokens (for demo purposes)
    query_token: str = "jessica"
    header_token: str = "fake-super-secret-token"


# Global settings instance
settings = Settings()
