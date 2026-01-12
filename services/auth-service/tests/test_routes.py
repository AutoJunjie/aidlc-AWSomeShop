"""Tests for API routes"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_root_endpoint(client: AsyncClient):
    """Test root endpoint"""
    response = await client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "auth-service"
    assert data["status"] == "running"


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    """Test health check endpoint"""
    response = await client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, test_user):
    """Test successful login"""
    response = await client.post(
        "/api/auth/login",
        json={"username": "testuser", "password": "Test1234"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert data["user"]["username"] == "testuser"
    assert data["user"]["role"] == "employee"


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient, test_user):
    """Test login with wrong password"""
    response = await client.post(
        "/api/auth/login",
        json={"username": "testuser", "password": "WrongPassword"}
    )
    
    assert response.status_code == 401
    data = response.json()
    assert "用户名或密码错误" in data["detail"]


@pytest.mark.asyncio
async def test_login_nonexistent_user(client: AsyncClient):
    """Test login with nonexistent user"""
    response = await client.post(
        "/api/auth/login",
        json={"username": "nonexistent", "password": "Test1234"}
    )
    
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_empty_username(client: AsyncClient):
    """Test login with empty username"""
    response = await client.post(
        "/api/auth/login",
        json={"username": "", "password": "Test1234"}
    )
    
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_login_empty_password(client: AsyncClient):
    """Test login with empty password"""
    response = await client.post(
        "/api/auth/login",
        json={"username": "testuser", "password": ""}
    )
    
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_login_case_insensitive_username(client: AsyncClient, test_user):
    """Test that login username is case insensitive"""
    response = await client.post(
        "/api/auth/login",
        json={"username": "TESTUSER", "password": "Test1234"}
    )
    
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_login_inactive_user(client: AsyncClient, inactive_user):
    """Test login with inactive user"""
    response = await client.post(
        "/api/auth/login",
        json={"username": "inactive", "password": "Test1234"}
    )
    
    assert response.status_code == 401
    data = response.json()
    assert "账户已禁用" in data["detail"]


@pytest.mark.asyncio
async def test_register_success(client: AsyncClient):
    """Test successful user registration"""
    response = await client.post(
        "/api/auth/register",
        json={"username": "newuser", "password": "New12345"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["user"]["username"] == "newuser"
    assert data["user"]["points_balance"] == 0


@pytest.mark.asyncio
async def test_register_first_user_is_admin(client: AsyncClient):
    """Test that first user becomes admin"""
    response = await client.post(
        "/api/auth/register",
        json={"username": "firstadmin", "password": "Admin1234"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["user"]["role"] == "admin"


@pytest.mark.asyncio
async def test_register_duplicate_username(client: AsyncClient, test_user):
    """Test registering with duplicate username"""
    response = await client.post(
        "/api/auth/register",
        json={"username": "testuser", "password": "Test1234"}
    )
    
    assert response.status_code == 409
    data = response.json()
    assert "用户名已存在" in data["detail"]


@pytest.mark.asyncio
async def test_register_invalid_username_format(client: AsyncClient):
    """Test registering with invalid username format"""
    response = await client.post(
        "/api/auth/register",
        json={"username": "user@invalid", "password": "Test1234"}
    )
    
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_short_username(client: AsyncClient):
    """Test registering with too short username"""
    response = await client.post(
        "/api/auth/register",
        json={"username": "ab", "password": "Test1234"}
    )
    
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_short_password(client: AsyncClient):
    """Test registering with too short password"""
    response = await client.post(
        "/api/auth/register",
        json={"username": "newuser", "password": "Test12"}
    )
    
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_no_uppercase_password(client: AsyncClient):
    """Test registering with password missing uppercase"""
    response = await client.post(
        "/api/auth/register",
        json={"username": "newuser", "password": "test1234"}
    )
    
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_no_lowercase_password(client: AsyncClient):
    """Test registering with password missing lowercase"""
    response = await client.post(
        "/api/auth/register",
        json={"username": "newuser", "password": "TEST1234"}
    )
    
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_no_digit_password(client: AsyncClient):
    """Test registering with password missing digit"""
    response = await client.post(
        "/api/auth/register",
        json={"username": "newuser", "password": "TestTest"}
    )
    
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_me_success(client: AsyncClient, test_user, auth_headers):
    """Test getting current user profile"""
    response = await client.get("/api/auth/me", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["role"] == "employee"
    assert data["points_balance"] == 100


@pytest.mark.asyncio
async def test_get_me_no_token(client: AsyncClient):
    """Test getting current user without token"""
    response = await client.get("/api/auth/me")
    
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_me_invalid_token(client: AsyncClient):
    """Test getting current user with invalid token"""
    response = await client.get(
        "/api/auth/me",
        headers={"Authorization": "Bearer invalid-token"}
    )
    
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_verify_token_success(client: AsyncClient, test_user, auth_headers):
    """Test token verification endpoint"""
    response = await client.get("/api/auth/verify", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"


@pytest.mark.asyncio
async def test_verify_token_invalid(client: AsyncClient):
    """Test token verification with invalid token"""
    response = await client.get(
        "/api/auth/verify",
        headers={"Authorization": "Bearer invalid-token"}
    )
    
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_verify_token_no_auth(client: AsyncClient):
    """Test token verification without authentication"""
    response = await client.get("/api/auth/verify")
    
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_admin_token_verification(client: AsyncClient, test_admin, admin_headers):
    """Test admin user token verification"""
    response = await client.get("/api/auth/verify", headers=admin_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["role"] == "admin"
