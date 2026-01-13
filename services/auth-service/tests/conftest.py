"""Test fixtures and configuration"""
import pytest
import asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.main import app
from app.database import Base, get_db
from app.models import User, RoleEnum
from app.security import hash_password

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False
)

test_async_session_maker = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def db_session():
    """Create a fresh database session for each test"""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with test_async_session_maker() as session:
        yield session
    
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def client(db_session):
    """Create test client with overridden database dependency"""
    
    async def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()


@pytest.fixture
async def test_user(db_session):
    """Create a test user"""
    user = User(
        username="testuser",
        password_hash=hash_password("Test1234"),
        role=RoleEnum.EMPLOYEE,
        points_balance=100,
        is_active=True
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture
async def test_admin(db_session):
    """Create a test admin user"""
    admin = User(
        username="admin",
        password_hash=hash_password("Admin1234"),
        role=RoleEnum.ADMIN,
        points_balance=0,
        is_active=True
    )
    db_session.add(admin)
    await db_session.commit()
    await db_session.refresh(admin)
    return admin


@pytest.fixture
async def inactive_user(db_session):
    """Create an inactive test user"""
    user = User(
        username="inactive",
        password_hash=hash_password("Test1234"),
        role=RoleEnum.EMPLOYEE,
        points_balance=0,
        is_active=False
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture
def auth_headers(test_user):
    """Create authentication headers with token"""
    from app.security import create_access_token
    token = create_access_token({
        "user_id": test_user.id,
        "username": test_user.username,
        "role": test_user.role.value
    })
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def admin_headers(test_admin):
    """Create authentication headers with admin token"""
    from app.security import create_access_token
    token = create_access_token({
        "user_id": test_admin.id,
        "username": test_admin.username,
        "role": test_admin.role.value
    })
    return {"Authorization": f"Bearer {token}"}
