import os
from typing import List


class Settings:
    """Application Settings and Environment Configuration."""

    APP_NAME: str = os.getenv("APP_NAME", "Adhikar Setu API")
    APP_ENV: str = os.getenv("APP_ENV", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() in ("true", "1", "t")
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", "8000"))
    API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]


settings = Settings()
