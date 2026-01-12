from pydantic import BaseModel, Field, field_validator
from typing import Optional
from app.config import settings


class LoginRequest(BaseModel):
    """登录请求"""
    username: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=settings.password_min_length)


class UserResponse(BaseModel):
    """用户响应"""
    id: int
    username: str
    role: str

    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    """登录响应"""
    token: str
    user: UserResponse


class UserMeResponse(BaseModel):
    """当前用户信息响应"""
    id: int
    username: str
    role: str
    points_balance: int

    class Config:
        from_attributes = True


class LogoutResponse(BaseModel):
    """登出响应"""
    message: str = "Logged out successfully"


class VerifyResponse(BaseModel):
    """Token 验证响应"""
    valid: bool
    user_id: Optional[int] = None
    role: Optional[str] = None
    error: Optional[str] = None


class HealthResponse(BaseModel):
    """健康检查响应"""
    status: str
    database: str


class ErrorResponse(BaseModel):
    """错误响应"""
    error_code: str
    message: str
    detail: Optional[str] = None
