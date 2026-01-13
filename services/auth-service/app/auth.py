"""Authentication business logic"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException, status
from app.models import User, RoleEnum
from app.schemas import LoginRequest, RegisterRequest, UserResponse, TokenResponse, RegisterResponse
from app.security import hash_password, verify_password, create_access_token
import logging
import json

logger = logging.getLogger(__name__)


async def authenticate_user(db: AsyncSession, login_data: LoginRequest, client_ip: str, user_agent: str) -> TokenResponse:
    """Authenticate user and return JWT token"""
    
    username_lower = login_data.username.lower()
    
    result = await db.execute(
        select(User).where(func.lower(User.username) == username_lower)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        log_login_failure(login_data.username, client_ip, user_agent, "用户不存在")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )
    
    if not user.is_active:
        log_login_failure(login_data.username, client_ip, user_agent, "账户已禁用")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="账户已禁用"
        )
    
    if not verify_password(login_data.password, user.password_hash):
        log_login_failure(login_data.username, client_ip, user_agent, "密码错误")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )
    
    token = create_access_token({
        "user_id": user.id,
        "username": user.username,
        "role": user.role.value
    })
    
    log_login_success(user.username, client_ip, user_agent)
    
    user_response = UserResponse(
        id=user.id,
        username=user.username,
        role=user.role.value,
        points_balance=user.points_balance
    )
    
    return TokenResponse(token=token, user=user_response)


async def register_user(db: AsyncSession, register_data: RegisterRequest) -> RegisterResponse:
    """Register a new user"""
    
    username_lower = register_data.username.lower()
    
    result = await db.execute(
        select(User).where(func.lower(User.username) == username_lower)
    )
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="用户名已存在"
        )
    
    user_count_result = await db.execute(select(func.count(User.id)))
    user_count = user_count_result.scalar()
    
    role = RoleEnum.ADMIN if user_count == 0 else RoleEnum.EMPLOYEE
    
    hashed_password = hash_password(register_data.password)
    
    new_user = User(
        username=register_data.username,
        password_hash=hashed_password,
        role=role,
        points_balance=0,
        is_active=True
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    user_response = UserResponse(
        id=new_user.id,
        username=new_user.username,
        role=new_user.role.value,
        points_balance=new_user.points_balance
    )
    
    return RegisterResponse(user=user_response)


async def get_user_by_id(db: AsyncSession, user_id: int) -> User:
    """Get user by ID"""
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="账户已禁用"
        )
    
    return user


def log_login_success(username: str, ip: str, user_agent: str):
    """Log successful login attempt"""
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "level": "INFO",
        "event": "login_success",
        "username": username,
        "ip": ip,
        "user_agent": user_agent
    }
    logger.info(json.dumps(log_data))


def log_login_failure(username: str, ip: str, user_agent: str, reason: str):
    """Log failed login attempt"""
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "level": "WARN",
        "event": "login_failure",
        "username": username,
        "ip": ip,
        "user_agent": user_agent,
        "reason": reason
    }
    logger.warning(json.dumps(log_data))


def log_token_invalid(ip: str, reason: str):
    """Log invalid token attempt"""
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "level": "WARN",
        "event": "token_invalid",
        "ip": ip,
        "reason": reason
    }
    logger.warning(json.dumps(log_data))


from datetime import datetime
