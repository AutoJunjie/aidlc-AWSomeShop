"""Tests for database models"""
import pytest
from sqlalchemy import select
from app.models import User, RoleEnum
from app.security import hash_password


@pytest.mark.asyncio
async def test_create_user(db_session):
    """Test creating a user"""
    user = User(
        username="newuser",
        password_hash=hash_password("Password123"),
        role=RoleEnum.EMPLOYEE,
        points_balance=0,
        is_active=True
    )
    
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    
    assert user.id is not None
    assert user.username == "newuser"
    assert user.role == RoleEnum.EMPLOYEE
    assert user.points_balance == 0
    assert user.is_active is True
    assert user.created_at is not None
    assert user.updated_at is not None


@pytest.mark.asyncio
async def test_user_default_values(db_session):
    """Test user default values"""
    user = User(
        username="defaultuser",
        password_hash=hash_password("Password123")
    )
    
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    
    assert user.role == RoleEnum.EMPLOYEE
    assert user.points_balance == 0
    assert user.is_active is True


@pytest.mark.asyncio
async def test_username_uniqueness(db_session):
    """Test that username must be unique"""
    user1 = User(
        username="uniqueuser",
        password_hash=hash_password("Password123")
    )
    db_session.add(user1)
    await db_session.commit()
    
    user2 = User(
        username="uniqueuser",
        password_hash=hash_password("Password456")
    )
    db_session.add(user2)
    
    with pytest.raises(Exception):
        await db_session.commit()


@pytest.mark.asyncio
async def test_admin_role(db_session):
    """Test creating admin user"""
    admin = User(
        username="admin",
        password_hash=hash_password("Admin123"),
        role=RoleEnum.ADMIN
    )
    
    db_session.add(admin)
    await db_session.commit()
    await db_session.refresh(admin)
    
    assert admin.role == RoleEnum.ADMIN


@pytest.mark.asyncio
async def test_query_user_by_username(db_session):
    """Test querying user by username"""
    user = User(
        username="queryuser",
        password_hash=hash_password("Password123")
    )
    db_session.add(user)
    await db_session.commit()
    
    result = await db_session.execute(
        select(User).where(User.username == "queryuser")
    )
    found_user = result.scalar_one_or_none()
    
    assert found_user is not None
    assert found_user.username == "queryuser"


@pytest.mark.asyncio
async def test_user_inactive_status(db_session):
    """Test setting user as inactive"""
    user = User(
        username="inactiveuser",
        password_hash=hash_password("Password123"),
        is_active=False
    )
    
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    
    assert user.is_active is False


@pytest.mark.asyncio
async def test_update_points_balance(db_session):
    """Test updating user points balance"""
    user = User(
        username="pointsuser",
        password_hash=hash_password("Password123"),
        points_balance=100
    )
    db_session.add(user)
    await db_session.commit()
    
    user.points_balance = 200
    await db_session.commit()
    await db_session.refresh(user)
    
    assert user.points_balance == 200


@pytest.mark.asyncio
async def test_role_enum_values():
    """Test role enum values"""
    assert RoleEnum.EMPLOYEE.value == "employee"
    assert RoleEnum.ADMIN.value == "admin"
