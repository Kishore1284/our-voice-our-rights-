"""
Application Configuration using Pydantic Settings
"""

from functools import lru_cache
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # App Info
    app_name: str = "Our Voice, Our Rights"
    environment: str = "development"
    debug: bool = True
    
    # Database
    database_url: str = "postgresql://mgnrega_user:mgnrega_pass@postgres:5432/mgnrega_db"
    
    # Redis
    redis_url: str = "redis://redis:6379/0"
    
    # MGNREGA API
    api_key: str = ""
    mgnrega_api_base_url: str = "https://api.data.gov.in/resource"
    
    # CORS
    cors_origins: List[str] = ["*"]
    
    # Cache
    cache_ttl: int = 3600  # 1 hour in seconds
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance (singleton pattern)"""
    return Settings()

