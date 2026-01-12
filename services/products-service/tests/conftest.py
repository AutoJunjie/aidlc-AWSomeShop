"""Test configuration and fixtures."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db
from app.models import Base
from app.config import settings
from unittest.mock import Mock, patch

# Use in-memory SQLite for testing
TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create test client with overridden database dependency."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def mock_auth_user():
    """Mock authenticated user."""
    return {
        "user_id": 1,
        "username": "testuser",
        "role": "user"
    }


@pytest.fixture
def mock_auth_admin():
    """Mock authenticated admin user."""
    return {
        "user_id": 2,
        "username": "admin",
        "role": "admin"
    }


@pytest.fixture
def mock_s3_service():
    """Mock S3 service."""
    with patch('app.services.s3_service.s3_service') as mock:
        mock.upload_file.return_value = "https://s3.example.com/products/1/test.jpg"
        mock.delete_file.return_value = True
        mock.check_connection.return_value = True
        yield mock


@pytest.fixture
def sample_product_data():
    """Sample product data for testing."""
    return {
        "name": "Test Product",
        "description": "Test Description",
        "points_cost": 100
    }
