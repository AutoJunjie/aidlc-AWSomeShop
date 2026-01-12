"""Tests for authentication business logic"""
import pytest
from fastapi import HTTPException
from app.auth import authenticate_user, register_user, get_user_by_id
from app.schemas import LoginRequest, RegisterRequest
from app.models import User, RoleEnum
from sqlalchemy import select


@pytest.mark.asyncio
async def test_authenticate_user_success(db_session, test_user):
    """Test successful user authentication"""
    login_data = LoginRequest(username="testuser", password="Test1234")
    
    result = await authenticate_user(db_session, login_data, "127.0.0.1", "test-agent")
    
    assert result.token is not None
    assert result.user.username == "testuser"
    assert result.user.role == "employee"


@pytest.mark.asyncio
async def test_authenticate_user_case_insensitive(db_session, test_user):
    """Test that username is case insensitive"""
    login_data = LoginRequest(username="TESTUSER", password="Test1234")
    
    result = await authenticate_user(db_session, login_data, "127.0.0.1", "test-agent")
    
    assert result.user.username == "testuser"


@pytest.mark.asyncio
async def test_authenticate_user_wrong_password(db_session, test_user):
    """Test authentication with wrong password"""
    login_data = LoginRequest(username="testuser", password="WrongPassword")
    
    with pytest.raises(HTTPException) as exc_info:
        await authenticate_user(db_session, login_data, "127.0.0.1", "test-agent")
    
    assert exc_info.value.status_code == 401
    assert "用户名或密码错误" in exc_info.value.detail


@pytest.mark.asyncio
async def test_authenticate_user_nonexistent(db_session):
    """Test authentication with nonexistent user"""
    login_data = LoginRequest(username="nonexistent", password="Test1234")
    
    with pytest.raises(HTTPException) as exc_info:
        await authenticate_user(db_session, login_data, "127.0.0.1", "test-agent")
    
    assert exc_info.value.status_code == 401
    assert "用户名或密码错误" in exc_info.value.detail


@pytest.mark.asyncio
async def test_authenticate_inactive_user(db_session, inactive_user):
    """Test authentication with inactive user"""
    login_data = LoginRequest(username="inactive", password="Test1234")
    
    with pytest.raises(HTTPException) as exc_info:
        await authenticate_user(db_session, login_data, "127.0.0.1", "test-agent")
    
    assert exc_info.value.status_code == 401
    assert "账户已禁用" in exc_info.value.detail


@pytest.mark.asyncio
async def test_register_first_user_as_admin(db_session):
    """Test that first registered user becomes admin"""
    register_data = RegisterRequest(username="firstuser", password="First1234")
    
    result = await register_user(db_session, register_data)
    
    assert result.user.username == "firstuser"
    assert result.user.role == "admin"


@pytest.mark.asyncio
async def test_register_second_user_as_employee(db_session, test_admin):
    """Test that second user becomes employee"""
    register_data = RegisterRequest(username="seconduser", password="Second1234")
    
    result = await register_user(db_session, register_data)
    
    assert result.user.username == "seconduser"
    assert result.user.role == "employee"


@pytest.mark.asyncio
async def test_register_duplicate_username(db_session, test_user):
    """Test registering with duplicate username"""
    register_data = RegisterRequest(username="testuser", password="Test1234")
    
    with pytest.raises(HTTPException) as exc_info:
        await register_user(db_session, register_data)
    
    assert exc_info.value.status_code == 409
    assert "用户名已存在" in exc_info.value.detail


@pytest.mark.asyncio
async def test_register_case_insensitive_duplicate(db_session, test_user):
    """Test that username uniqueness is case insensitive"""
    register_data = RegisterRequest(username="TESTUSER", password="Test1234")
    
    with pytest.raises(HTTPException) as exc_info:
        await register_user(db_session, register_data)
    
    assert exc_info.value.status_code == 409


@pytest.mark.asyncio
async def test_register_user_default_points(db_session):
    """Test that new user has default points balance"""
    register_data = RegisterRequest(username="newuser", password="New12345")
    
    result = await register_user(db_session, register_data)
    
    assert result.user.points_balance == 0


@pytest.mark.asyncio
async def test_get_user_by_id_success(db_session, test_user):
    """Test getting user by ID"""
    user = await get_user_by_id(db_session, test_user.id)
    
    assert user.id == test_user.id
    assert user.username == test_user.username


@pytest.mark.asyncio
async def test_get_user_by_id_nonexistent(db_session):
    """Test getting nonexistent user by ID"""
    with pytest.raises(HTTPException) as exc_info:
        await get_user_by_id(db_session, 99999)
    
    assert exc_info.value.status_code == 401
    assert "用户不存在" in exc_info.value.detail


@pytest.mark.asyncio
async def test_get_inactive_user_by_id(db_session, inactive_user):
    """Test getting inactive user by ID"""
    with pytest.raises(HTTPException) as exc_info:
        await get_user_by_id(db_session, inactive_user.id)
    
    assert exc_info.value.status_code == 401
    assert "账户已禁用" in exc_info.value.detail


@pytest.mark.asyncio
async def test_password_is_hashed(db_session):
    """Test that password is hashed when registering"""
    register_data = RegisterRequest(username="hashtest", password="Hash1234")
    
    result = await register_user(db_session, register_data)
    
    db_result = await db_session.execute(
        select(User).where(User.id == result.user.id)
    )
    user = db_result.scalar_one()
    
    assert user.password_hash != "Hash1234"
    assert user.password_hash.startswith("$2b$")
