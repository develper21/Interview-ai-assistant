"""
Configuration settings for the Interview AI Backend
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings with environment variable support"""

    # API Configuration
    api_title: str = Field(default="Interview AI API", env="API_TITLE")
    api_description: str = Field(
        default="Professional API for Interview AI platform with content management",
        env="API_DESCRIPTION"
    )
    api_version: str = Field(default="1.0.0", env="API_VERSION")
    api_host: str = Field(default="localhost", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")
    api_debug: bool = Field(default=True, env="API_DEBUG")

    # Security
    secret_key: str = Field(default="your-secret-key-change-in-production", env="SECRET_KEY")
    algorithm: str = Field(default="HS256", env="ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")

    # Database
    database_url: str = Field(
        default="postgresql://user:password@localhost/interview_ai",
        env="DATABASE_URL"
    )
    database_pool_size: int = Field(default=10, env="DATABASE_POOL_SIZE")
    database_max_overflow: int = Field(default=20, env="DATABASE_MAX_OVERFLOW")

    # Google AI Services
    google_api_key: str = Field(default="", env="GOOGLE_API_KEY")
    google_project_id: str = Field(default="", env="GOOGLE_PROJECT_ID")
    google_speech_credentials_path: Optional[str] = Field(default=None, env="GOOGLE_APPLICATION_CREDENTIALS")

    # File Storage
    upload_dir: str = Field(default="uploads", env="UPLOAD_DIR")
    max_file_size: int = Field(default=10 * 1024 * 1024, env="MAX_FILE_SIZE")  # 10MB
    allowed_extensions: list = Field(
        default=[".jpg", ".jpeg", ".png", ".gif", ".pdf", ".doc", ".docx"],
        env="ALLOWED_EXTENSIONS"
    )

    # CORS
    cors_origins: list = Field(
        default=["http://localhost:3000", "http://127.0.0.1:3000"],
        env="CORS_ORIGINS"
    )

    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        env="LOG_FORMAT"
    )

    # Redis (for caching and sessions)
    redis_url: Optional[str] = Field(default=None, env="REDIS_URL")
    redis_host: str = Field(default="localhost", env="REDIS_HOST")
    redis_port: int = Field(default=6379, env="REDIS_PORT")
    redis_db: int = Field(default=0, env="REDIS_DB")

    # Email Configuration (for notifications)
    smtp_server: Optional[str] = Field(default=None, env="SMTP_SERVER")
    smtp_port: int = Field(default=587, env="SMTP_PORT")
    smtp_username: Optional[str] = Field(default=None, env="SMTP_USERNAME")
    smtp_password: Optional[str] = Field(default=None, env="SMTP_PASSWORD")
    email_from: str = Field(default="noreply@interviewai.com", env="EMAIL_FROM")

    # External APIs
    gemini_model: str = Field(default="gemini-pro", env="GEMINI_MODEL")
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()


def get_database_url() -> str:
    """Get database URL, with fallback for SQLite in development"""
    if settings.database_url.startswith("postgresql://"):
        return settings.database_url
    elif os.getenv("ENVIRONMENT") == "development":
        return "sqlite:///./interview_ai.db"
    return settings.database_url


def get_cors_origins() -> list:
    """Get CORS origins as list"""
    if isinstance(settings.cors_origins, str):
        return [origin.strip() for origin in settings.cors_origins.split(",")]
    return settings.cors_origins


def create_directories():
    """Create necessary directories on startup"""
    os.makedirs(settings.upload_dir, exist_ok=True)
    os.makedirs("logs", exist_ok=True)
