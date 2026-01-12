"""Tests for Pydantic schemas"""
import pytest
from pydantic import ValidationError
from app.schemas import LoginRequest, RegisterRequest, UserResponse, TokenResponse


def test_login_request_valid():
    """Test valid login request"""
    login = LoginRequest(username="testuser", password="password123")
    
    assert login.username == "testuser"
    assert login.password == "password123"


def test_login_request_empty_username():
    """Test login request with empty username"""
    with pytest.raises(ValidationError):
        LoginRequest(username="", password="password123")


def test_login_request_empty_password():
    """Test login request with empty password"""
    with pytest.raises(ValidationError):
        LoginRequest(username="testuser", password="")


def test_register_request_valid():
    """Test valid registration request"""
    register = RegisterRequest(username="newuser", password="Test1234")
    
    assert register.username == "newuser"
    assert register.password == "Test1234"


def test_register_request_username_too_short():
    """Test registration with username too short"""
    with pytest.raises(ValidationError):
        RegisterRequest(username="ab", password="Test1234")


def test_register_request_username_too_long():
    """Test registration with username too long"""
    with pytest.raises(ValidationError):
        RegisterRequest(username="a" * 51, password="Test1234")


def test_register_request_username_invalid_chars():
    """Test registration with invalid username characters"""
    with pytest.raises(ValidationError) as exc_info:
        RegisterRequest(username="user@test", password="Test1234")
    
    assert "用户名只能包含字母、数字和下划线" in str(exc_info.value)


def test_register_request_password_too_short():
    """Test registration with password too short"""
    with pytest.raises(ValidationError):
        RegisterRequest(username="testuser", password="Test12")


def test_register_request_password_no_uppercase():
    """Test registration with password missing uppercase letter"""
    with pytest.raises(ValidationError) as exc_info:
        RegisterRequest(username="testuser", password="test1234")
    
    assert "大写字母" in str(exc_info.value)


def test_register_request_password_no_lowercase():
    """Test registration with password missing lowercase letter"""
    with pytest.raises(ValidationError) as exc_info:
        RegisterRequest(username="testuser", password="TEST1234")
    
    assert "小写字母" in str(exc_info.value)


def test_register_request_password_no_digit():
    """Test registration with password missing digit"""
    with pytest.raises(ValidationError) as exc_info:
        RegisterRequest(username="testuser", password="TestTest")
    
    assert "数字" in str(exc_info.value)


def test_register_request_valid_complex_password():
    """Test registration with valid complex password"""
    register = RegisterRequest(username="testuser", password="Test@1234")
    
    assert register.password == "Test@1234"


def test_user_response_creation():
    """Test UserResponse creation"""
    user_response = UserResponse(
        id=1,
        username="testuser",
        role="employee",
        points_balance=100
    )
    
    assert user_response.id == 1
    assert user_response.username == "testuser"
    assert user_response.role == "employee"
    assert user_response.points_balance == 100


def test_token_response_creation():
    """Test TokenResponse creation"""
    user_response = UserResponse(
        id=1,
        username="testuser",
        role="employee",
        points_balance=100
    )
    
    token_response = TokenResponse(
        token="fake-token",
        user=user_response
    )
    
    assert token_response.token == "fake-token"
    assert token_response.user.username == "testuser"


def test_username_with_underscores():
    """Test that username can contain underscores"""
    register = RegisterRequest(username="test_user_123", password="Test1234")
    
    assert register.username == "test_user_123"


def test_username_with_numbers():
    """Test that username can contain numbers"""
    register = RegisterRequest(username="user123", password="Test1234")
    
    assert register.username == "user123"


def test_username_alphanumeric():
    """Test that username can be alphanumeric"""
    register = RegisterRequest(username="testUser123", password="Test1234")
    
    assert register.username == "testUser123"
