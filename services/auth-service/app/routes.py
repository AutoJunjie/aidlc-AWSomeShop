"""API route definitions"""
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas import (
    LoginRequest, RegisterRequest, TokenResponse, 
    RegisterResponse, UserResponse, HealthResponse
)
from app.auth import authenticate_user, register_user
from app.dependencies import get_current_user
from app.models import User

router = APIRouter()


@router.post("/api/auth/login", response_model=TokenResponse)
async def login(
    request: Request,
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """User login endpoint"""
    client_ip = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "unknown")
    
    return await authenticate_user(db, login_data, client_ip, user_agent)


@router.post("/api/auth/register", response_model=RegisterResponse)
async def register(
    register_data: RegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    """User registration endpoint"""
    return await register_user(db, register_data)


@router.get("/api/auth/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current user profile from JWT token"""
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        role=current_user.role.value,
        points_balance=current_user.points_balance
    )


@router.get("/api/auth/verify", response_model=UserResponse)
async def verify_token(current_user: User = Depends(get_current_user)):
    """Internal endpoint for token verification"""
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        role=current_user.role.value,
        points_balance=current_user.points_balance
    )


@router.get("/health", response_model=HealthResponse)
async def health_check(db: AsyncSession = Depends(get_db)):
    """Health check endpoint"""
    try:
        await db.execute("SELECT 1")
        return HealthResponse(status="healthy", database="connected")
    except Exception:
        return HealthResponse(status="unhealthy", database="disconnected")
