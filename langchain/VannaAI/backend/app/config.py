from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


BACKEND_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BACKEND_DIR / ".env")


class Settings(BaseSettings):
    database_url: str
    app_database_url: str | None = None
    deepseek_api_key: str | None = None
    deepseek_base_url: str = "https://api.deepseek.com/v1"
    openai_api_key: str | None = None
    openai_base_url: str = "https://api.openai.com/v1"
    vanna_model: str = "deepseek-chat"
    backend_cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
    query_row_limit: int = 200

    model_config = SettingsConfigDict(env_file=BACKEND_DIR / ".env", extra="ignore")

    @property
    def resolved_app_database_url(self) -> str:
        return self.app_database_url or self.database_url

    @property
    def cors_origins(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.backend_cors_origins.split(",")
            if origin.strip()
        ]

    @property
    def business_tables(self) -> list[str]:
        return ["customers", "products", "orders", "order_items", "payments", "refunds"]

    @property
    def llm_config(self) -> dict[str, str]:
        api_key = self.deepseek_api_key or self.openai_api_key
        if not api_key:
            raise RuntimeError("DEEPSEEK_API_KEY or OPENAI_API_KEY is required.")

        using_deepseek = bool(self.deepseek_api_key)
        default_base_url = self.deepseek_base_url if using_deepseek else self.openai_base_url
        model = self.vanna_model or ("deepseek-chat" if using_deepseek else "gpt-4o-mini")
        return {
            "api_key": api_key,
            "base_url": os.getenv("DEEPSEEK_BASE_URL" if using_deepseek else "OPENAI_BASE_URL", default_base_url),
            "model": model,
        }


@lru_cache
def get_settings() -> Settings:
    return Settings()
