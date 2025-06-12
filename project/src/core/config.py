from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    DATABASE_URL: str
    SQL_ECHO: bool = False
    PROJECT_NAME: str = "Library Management System"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 11520
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:8000", "http://localhost:3000"]

    class Config:
        env_file = ".env"


settings = Settings()
