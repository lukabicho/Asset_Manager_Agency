from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Asset Manager"

    DATABASE_URL: str
    MONGODB_URL: str
    REDIS_URL: str

    MINIO_URL: str
    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: str
    MINIO_DEFAULT_BUCKET: str = "assets"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()