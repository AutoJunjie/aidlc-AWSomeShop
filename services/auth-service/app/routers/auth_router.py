from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import Optional
import logging
import json
from datetime import datetime

from app.database import get_db
from app.models import User
from app.schemas import (
    LoginRequest, LoginResponse, UserResponse,
    LogoutResponse, UserMeResponse, VerifyResponse,
    ErrorResponse
)
from app.auth import (
    verify_password, create_access_token,
    decode_access_token, extract_token_from_header
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/auth", tags=["auth"])


# 错误消息常量
class ErrorCodes:
    AUTH001 = "AUTH001"  # Invalid credentials
    AUTH002 = "AUTH002"  # Token expired
    AUTH003 = "AUTH003"  # Invalid token
    AUTH004 = "AUTH004"  # Missing token
    AUTH005 = "AUTH005"  # User not found


ERROR_MESSAGES = {
    ErrorCodes.AUTH001: "Invalid username or password",
    ErrorCodes.AUTH002: "Token expired",
    ErrorCodes.AUTH003: "Invalid token",
    ErrorCodes.AUTH004: "Missing token",
    ErrorCodes.AUTH005: "User not found",
}


def log_event(event: str, **kwargs):
    """记录结构化日志"""
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "service": "auth-service",
        "event": event,
        **kwargs
    }
    logger.info(json.dumps(log_data))


def get_current_user_from_token(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> User:
    """
    从 token 获取当前用户（依赖注入）
    
    Args:
        authorization: Authorization header
        db: 数据库会话
        
    Returns:
        User: 当前用户
        
    Raises:
        HTTPException: token 无效或用户不存在
    """
    if not authorization:
        log_event("auth_missing_token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error_code": ErrorCodes.AUTH004,
                "message": ERROR_MESSAGES[ErrorCodes.AUTH004]
            }
        )
    
    token = extract_token_from_header(authorization)
    if not token:
        log_event("auth_invalid_token_format")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error_code": ErrorCodes.AUTH003,
                "message": ERROR_MESSAGES[ErrorCodes.AUTH003]
            }
        )
    
    payload = decode_access_token(token)
    if not payload:
        log_event("auth_token_decode_failed")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error_code": ErrorCodes.AUTH003,
                "message": ERROR_MESSAGES[ErrorCodes.AUTH003]
            }
        )
    
    user_id = payload.get("sub")
    if not user_id:
        log_event("auth_invalid_token_payload")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error_code": ErrorCodes.AUTH003,
                "message": ERROR_MESSAGES[ErrorCodes.AUTH003]
            }
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        log_event("auth_user_not_found", user_id=user_id)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error_code": ErrorCodes.AUTH005,
                "message": ERROR_MESSAGES[ErrorCodes.AUTH005]
            }
        )
    
    return user


@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    用户登录
    
    Args:
        request: 登录请求（username, password）
        db: 数据库会话
        
    Returns:
        LoginResponse: 包含 token 和用户信息
        
    Raises:
        HTTPException: 登录失败
    """
    # 验证必填字段（由 Pydantic 自动处理）
    
    # 查询用户
    user = db.query(User).filter(User.username == request.username).first()
    
    # 验证用户和密码
    if not user or not verify_password(request.password, user.password_hash):
        log_event("login_attempt", username=request.username, success=False)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error_code": ErrorCodes.AUTH001,
                "message": ERROR_MESSAGES[ErrorCodes.AUTH001]
            }
        )
    
    # 创建 JWT token
    token_data = {
        "sub": str(user.id),
        "username": user.username,
        "role": user.role
    }
    token = create_access_token(token_data)
    
    log_event("login_attempt", username=request.username, success=True, user_id=user.id)
    
    return LoginResponse(
        token=token,
        user=UserResponse(
            id=user.id,
            username=user.username,
            role=user.role
        )
    )


@router.post("/logout", response_model=LogoutResponse, status_code=status.HTTP_200_OK)
async def logout(
    current_user: User = Depends(get_current_user_from_token)
):
    """
    用户登出
    
    Args:
        current_user: 当前用户（从 token 解析）
        
    Returns:
        LogoutResponse: 登出成功消息
        
    Note:
        MVP 阶段不实现 token 黑名单，客户端负责清除本地 token
    """
    log_event("logout", user_id=current_user.id, username=current_user.username)
    return LogoutResponse(message="Logged out successfully")


@router.get("/me", response_model=UserMeResponse, status_code=status.HTTP_200_OK)
async def get_me(
    current_user: User = Depends(get_current_user_from_token)
):
    """
    获取当前用户信息
    
    Args:
        current_user: 当前用户（从 token 解析）
        
    Returns:
        UserMeResponse: 当前用户信息（包括积分余额）
    """
    log_event("get_me", user_id=current_user.id, username=current_user.username)
    return UserMeResponse(
        id=current_user.id,
        username=current_user.username,
        role=current_user.role,
        points_balance=current_user.points_balance
    )


@router.get("/verify", response_model=VerifyResponse)
async def verify_token(
    authorization: Optional[str] = Header(None)
):
    """
    验证 token 有效性（服务间调用）
    
    Args:
        authorization: Authorization header
        
    Returns:
        VerifyResponse: 验证结果
    """
    if not authorization:
        log_event("verify_token", valid=False, reason="missing_token")
        return VerifyResponse(
            valid=False,
            error="Invalid or expired token"
        )
    
    token = extract_token_from_header(authorization)
    if not token:
        log_event("verify_token", valid=False, reason="invalid_format")
        return VerifyResponse(
            valid=False,
            error="Invalid or expired token"
        )
    
    payload = decode_access_token(token)
    if not payload:
        log_event("verify_token", valid=False, reason="decode_failed")
        return VerifyResponse(
            valid=False,
            error="Invalid or expired token"
        )
    
    user_id = payload.get("sub")
    role = payload.get("role")
    
    if not user_id or not role:
        log_event("verify_token", valid=False, reason="invalid_payload")
        return VerifyResponse(
            valid=False,
            error="Invalid or expired token"
        )
    
    log_event("verify_token", valid=True, user_id=user_id, role=role)
    return VerifyResponse(
        valid=True,
        user_id=int(user_id),
        role=role
    )
