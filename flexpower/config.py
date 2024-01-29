import os
from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application Settings"""

    environment: str = os.getenv("ENVIRONMENT", "dev")
    testing: bool = False


@lru_cache()
def get_settings() -> BaseSettings:
    """
    Retrieves and caches application settings from the environment.

    Returns:
        BaseSettings: An instance containing the loaded settings.
    """
    return Settings()
