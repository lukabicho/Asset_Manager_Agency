"""This is an application configuration module"""
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Asset Manager"

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    DATABASE_URL: str
    # MONGODB_URL: str
    REDIS_URL: str

    MINIO_URL: str
    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: str
    MINIO_DEFAULT_BUCKET: str = "assets"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()