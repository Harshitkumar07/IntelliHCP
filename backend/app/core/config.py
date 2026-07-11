"""
Application configuration loaded from environment variables.

Uses pydantic-settings for type-safe config with .env file support.
All secrets (GROQ_API_KEY, DATABASE_URL) are loaded from environment,
never hardcoded.
"""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Centralised application settings sourced from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # ── Application ──────────────────────────────────────
    APP_NAME: str = "IntelliHCP"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"

    # ── Database ─────────────────────────────────────────
    DATABASE_URL: str = "sqlite:///./intellihcp.db"

    # ── Groq LLM ────────────────────────────────────────
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.3-70b-versatile"

    # ── CORS ─────────────────────────────────────────────
    CORS_ORIGINS: list[str] = ["http://localhost:5173"]


# Singleton — import this everywhere
settings = Settings()
