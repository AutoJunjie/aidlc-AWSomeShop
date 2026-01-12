"""Configuration management for Products Service."""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""
    
    # Database
    database_url: str = "postgresql://postgres:postgres@db:5432/awsomeshop"
    
    # Auth Service
    auth_service_url: str = "http://auth-service:8000"
    
    # AWS S3
    s3_bucket: str = "awsomeshop-products"
    aws_region: str = "us-east-1"
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    
    # App
    app_name: str = "Products Service"
    debug: bool = False
    log_level: str = "INFO"
    
    # File Upload
    max_file_size: int = 5 * 1024 * 1024  # 5MB
    allowed_file_types: list = ["image/jpeg", "image/png", "image/webp"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
