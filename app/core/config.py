from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # -------------------------------
    # APP CONFIG
    # -------------------------------
    APP_NAME: str = "SynCommerce AI"
    ENV: str = "development"
    DEBUG: bool = True

    # -------------------------------
    # SERVER
    # -------------------------------
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # -------------------------------
    # DATABASE
    # -------------------------------
    MONGO_URI: str
    DATABASE_NAME: str

    # -------------------------------
    # SECURITY
    # -------------------------------
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # -------------------------------
    # REDIS (future)
    # -------------------------------
    REDIS_URL: str = "redis://localhost:6379"

    # -------------------------------
    # LOGGING
    # -------------------------------
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()