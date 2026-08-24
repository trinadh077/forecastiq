from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    APP_NAME: str = "ForecastIQ"
    APP_ENV: str = "development"
    DEBUG: bool = False
    API_V1_STR: str = "/api/v1"
    
    SECRET_KEY: str = Field(default="super-secret-key-change-this-in-production-min-32-chars-long!")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "forecastiq"
    POSTGRES_PASSWORD: str = "forecastiq_password"
    POSTGRES_DB: str = "forecastiq_db"
    DATABASE_URL: str = Field(default="")

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_URL: str = Field(default="redis://localhost:6379/0")

    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://forecastiq-frontend.onrender.com",
        "https://forecastiq-00pd.onrender.com",
        "https://forecastiq-pcs2.onrender.com",
    ]

    S3_ENDPOINT_URL: str = "http://localhost:9000"
    AWS_ACCESS_KEY_ID: str = "minioadmin"
    AWS_SECRET_ACCESS_KEY: str = "minioadmin"
    S3_BUCKET_NAME: str = "forecastiq-datasets"
    AWS_REGION: str = "us-east-1"

settings = Settings()
