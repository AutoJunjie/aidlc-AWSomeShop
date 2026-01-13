"""Tests for FastAPI dependencies"""
import pytest
from fastapi import HTTPException
from unittest.mock import Mock, AsyncMock
from app.dependencies import get_current_user, require_admin
from app.models import User, RoleEnum
from app.security import create_access_token


@pytest.mark.asyncio
async def test_get_current_user_valid_token(db_session, test_user):
    """Test get_current_user with valid token"""
    token = create_access_token({
        "user_id": test_user.id,
        "username": test_user.username,
        "role": test_user.role.value
    })
    
    request = Mock()
    request.client.host = "127.0.0.1"
    
    credentials = Mock()
    credentials.credentials = token
    
    user = await get_current_user(request, credentials, db_session)
    
    assert user.id == test_user.id
    assert user.username == test_user.username


@pytest.mark.asyncio
async def test_get_current_user_invalid_token(db_session):
    """Test get_current_user with invalid token"""
    request = Mock()
    request.client.host = "127.0.0.1"
    
    credentials = Mock()
    credentials.credentials = "invalid-token"
    
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(request, credentials, db_session)
    
    assert exc_info.value.status_code == 401
    assert "无效的认证令牌" in exc_info.value.detail


@pytest.mark.asyncio
async def test_get_current_user_missing_user_id(db_session):
    """Test get_current_user with token missing user_id"""
    token = create_access_token({
        "username": "testuser",
        "role": "employee"
    })
    
    request = Mock()
    request.client.host = "127.0.0.1"
    
    credentials = Mock()
    credentials.credentials = token
    
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(request, credentials, db_session)
    
    assert exc_info.value.status_code == 401


@pytest.mark.asyncio
async def test_get_current_user_nonexistent_user(db_session):
    """Test get_current_user with token for nonexistent user"""
    token = create_access_token({
        "user_id": 99999,
        "username": "nonexistent",
        "role": "employee"
    })
    
    request = Mock()
    request.client.host = "127.0.0.1"
    
    credentials = Mock()
    credentials.credentials = token
    
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(request, credentials, db_session)
    
    assert exc_info.value.status_code == 401
    assert "用户不存在" in exc_info.value.detail


@pytest.mark.asyncio
async def test_get_current_user_inactive_user(db_session, inactive_user):
    """Test get_current_user with token for inactive user"""
    token = create_access_token({
        "user_id": inactive_user.id,
        "username": inactive_user.username,
        "role": inactive_user.role.value
    })
    
    request = Mock()
    request.client.host = "127.0.0.1"
    
    credentials = Mock()
    credentials.credentials = token
    
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(request, credentials, db_session)
    
    assert exc_info.value.status_code == 401
    assert "账户已禁用" in exc_info.value.detail


@pytest.mark.asyncio
async def test_require_admin_with_admin_user(test_admin):
    """Test require_admin with admin user"""
    user = await require_admin(test_admin)
    
    assert user.role == RoleEnum.ADMIN


@pytest.mark.asyncio
async def test_require_admin_with_employee_user(test_user):
    """Test require_admin with employee user"""
    with pytest.raises(HTTPException) as exc_info:
        await require_admin(test_user)
    
    assert exc_info.value.status_code == 403
    assert "权限不足" in exc_info.value.detail


@pytest.mark.asyncio
async def test_require_admin_permission_denied(db_session, test_user):
    """Test that employee cannot access admin endpoints"""
    with pytest.raises(HTTPException) as exc_info:
        await require_admin(test_user)
    
    assert exc_info.value.status_code == 403
