"""
Application settings and configuration management.
"""

import os
from typing import Dict, List, Optional

from pydantic import BaseSettings, Field, RedisDsn, AnyUrl


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Application
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")
    DEBUG: bool = Field(default=False, env="DEBUG")
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    
    # API
    API_HOST: str = Field(default="0.0.0.0", env="API_HOST")
    API_PORT: int = Field(default=8000, env="API_PORT")
    API_WORKERS: int = Field(default=4, env="API_WORKERS")
    
    # Redis
    REDIS_URL: RedisDsn = Field(
        default="redis://localhost:6379/0", env="REDIS_URL"
    )
    REDIS_MAX_CONNECTIONS: int = Field(default=20, env="REDIS_MAX_CONNECTIONS")
    
    # AI Models
    AI_DEVICE: str = Field(default="auto", env="AI_DEVICE")
    AI_MODEL_CACHE_DIR: str = Field(
        default="/tmp/gneiss-models", env="AI_MODEL_CACHE_DIR"
    )
    
    # Cloud Storage
    AWS_ACCESS_KEY_ID: Optional[str] = Field(env="AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: Optional[str] = Field(env="AWS_SECRET_ACCESS_KEY")
    AWS_S3_BUCKET: Optional[str] = Field(env="AWS_S3_BUCKET")
    
    GCP_PROJECT_ID: Optional[str] = Field(env="GCP_PROJECT_ID")
    GCP_BUCKET_NAME: Optional[str] = Field(env="GCP_BUCKET_NAME")
    
    # Monitoring
    OTEL_EXPORTER_OTLP_ENDPOINT: Optional[AnyUrl] = Field(
        env="OTEL_EXPORTER_OTLP_ENDPOINT"
    )
    PROMETHEUS_MULTIPROC_DIR: Optional[str] = Field(
        env="PROMETHEUS_MULTIPROC_DIR"
    )
    
    # Security
    JWT_SECRET_KEY: str = Field(
        default="change-me-in-production", env="JWT_SECRET_KEY"
    )
    JWT_ALGORITHM: str = Field(default="HS256", env="JWT_ALGORITHM")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30, env="JWT_ACCESS_TOKEN_EXPIRE_MINUTES"
    )
    
    # Rate limiting
    RATE_LIMIT_REQUESTS: int = Field(default=100, env="RATE_LIMIT_REQUESTS")
    RATE_LIMIT_WINDOW: int = Field(default=3600, env="RATE_LIMIT_WINDOW")
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.ENVIRONMENT == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.ENVIRONMENT == "development"
    
    @property
    def is_testing(self) -> bool:
        """Check if running in testing environment."""
        return self.ENVIRONMENT == "test"


# Global settings instance
settings = Settings()

# Environment-specific configurations
ENV_CONFIGS: Dict[str, Dict[str, any]] = {
    "development": {
        "DEBUG": True,
        "LOG_LEVEL": "DEBUG",
        "AI_DEVICE": "cpu",
    },
    "production": {
        "DEBUG": False,
        "LOG_LEVEL": "INFO",
        "AI_DEVICE": "cuda",
    },
    "test": {
        "DEBUG": True,
        "LOG_LEVEL": "DEBUG",
        "AI_DEVICE": "cpu",
    },
}