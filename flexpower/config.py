import os
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    environment: str = os.getenv("ENVIRONMENT", "dev")
    testing: bool = os.getenv("TESTING", True)  # type: ignore
    database_url: str = os.environ.get("DATABASE_URL")  # type: ignore
    http_username: str = os.environ.get("HTTP_USERNAME")
    http_password: str = os.environ.get("HTTP_PASSWORD")


@lru_cache()
def get_settings() -> BaseSettings:
    return Settings()
