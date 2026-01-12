"""Pydantic schemas for request/response validation"""
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional
import re


class LoginRequest(BaseModel):
    """Login request schema"""
    username: str = Field(..., min_length=1, description="用户名")
    password: str = Field(..., min_length=1, description="密码")


class RegisterRequest(BaseModel):
    """Registration request schema"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    password: str = Field(..., min_length=8, description="密码")
    
    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        """Validate username format"""
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('用户名只能包含字母、数字和下划线')
        return v
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password complexity"""
        if len(v) < 8:
            raise ValueError('密码至少需要8个字符')
        if not any(c.isupper() for c in v):
            raise ValueError('密码必须包含至少一个大写字母')
        if not any(c.islower() for c in v):
            raise ValueError('密码必须包含至少一个小写字母')
        if not any(c.isdigit() for c in v):
            raise ValueError('密码必须包含至少一个数字')
        return v


class UserResponse(BaseModel):
    """User response schema"""
    id: int
    username: str
    role: str
    points_balance: int
    
    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Token response schema"""
    token: str
    user: UserResponse


class RegisterResponse(BaseModel):
    """Registration response schema"""
    user: UserResponse


class HealthResponse(BaseModel):
    """Health check response schema"""
    status: str
    database: str


class TokenPayload(BaseModel):
    """JWT token payload schema"""
    user_id: int
    username: str
    role: str
    exp: int
    iat: int
