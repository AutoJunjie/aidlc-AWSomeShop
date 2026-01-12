"""Authentication middleware for JWT verification."""
from fastapi import Header, HTTPException, status
from typing import Optional
import requests
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class AuthenticationError(HTTPException):
    """Authentication error exception."""
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"}
        )


class AuthorizationError(HTTPException):
    """Authorization error exception."""
    def __init__(self, detail: str = "Insufficient permissions"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )


def verify_token(authorization: Optional[str] = Header(None)) -> dict:
    """
    Verify JWT token by calling auth service.
    
    Args:
        authorization: Authorization header (Bearer token)
    
    Returns:
        dict: User information from auth service
    
    Raises:
        AuthenticationError: If token is invalid or missing
    """
    if not authorization:
        raise AuthenticationError("Missing authorization header")
    
    if not authorization.startswith("Bearer "):
        raise AuthenticationError("Invalid authorization header format")
    
    token = authorization.split(" ")[1]
    
    try:
        # Call auth service to verify token
        response = requests.get(
            f"{settings.auth_service_url}/api/auth/verify",
            headers={"Authorization": f"Bearer {token}"},
            timeout=5
        )
        
        if response.status_code == 200:
            user_data = response.json()
            logger.info(f"Token verified for user: {user_data.get('user_id')}")
            return user_data
        elif response.status_code == 401:
            raise AuthenticationError("Invalid or expired token")
        else:
            logger.error(f"Auth service returned status {response.status_code}")
            raise AuthenticationError("Authentication failed")
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to connect to auth service: {e}")
        raise AuthenticationError("Authentication service unavailable")


def verify_admin(authorization: Optional[str] = Header(None)) -> dict:
    """
    Verify JWT token and check for admin role.
    
    Args:
        authorization: Authorization header (Bearer token)
    
    Returns:
        dict: User information from auth service
    
    Raises:
        AuthenticationError: If token is invalid or missing
        AuthorizationError: If user is not admin
    """
    user_data = verify_token(authorization)
    
    if user_data.get("role") != "admin":
        logger.warning(f"User {user_data.get('user_id')} attempted admin action without permission")
        raise AuthorizationError("Admin privileges required")
    
    return user_data


# Dependency functions for FastAPI
async def get_current_user(authorization: Optional[str] = Header(None)) -> dict:
    """FastAPI dependency for getting current user."""
    return verify_token(authorization)


async def get_admin_user(authorization: Optional[str] = Header(None)) -> dict:
    """FastAPI dependency for getting admin user."""
    return verify_admin(authorization)
