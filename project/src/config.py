from pydantic_settings import BaseSettings
from pydantic import validator

from typing import List, Optional, Union
import secrets


class Settings(BaseSettings):
    PROJECT_NAME: str = "Library Management System"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 jours
    SQL_ECHO: bool = False  # Activer l'écho SQL pour le débogage

    # CORS
    BACKEND_CORS_ORIGINS: Union[str, List[str]] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str):
            return [i.strip().strip('"') for i in v.strip("[]").split(",")]
        return v

    # Base de données
    DATABASE_URL: str = "sqlite:///./library.db"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()