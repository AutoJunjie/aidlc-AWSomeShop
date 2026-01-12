from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """应用配置"""
    # Database
    database_url: str = "postgresql://postgres:postgres@localhost:5432/awsomeshop"
    
    # JWT
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24
    
    # Logging
    log_level: str = "INFO"
    
    # Database Pool
    sqlalchemy_pool_size: int = 10
    sqlalchemy_max_overflow: int = 20
    sqlalchemy_pool_timeout: int = 30
    
    # Password
    bcrypt_salt_rounds: int = 12
    password_min_length: int = 8
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
