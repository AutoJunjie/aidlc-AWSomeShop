import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.models import User
from app.auth import hash_password, create_access_token

# 创建测试数据库
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """覆盖数据库依赖，使用测试数据库"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    """每个测试前创建表，测试后删除表"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_user():
    """创建测试用户"""
    db = TestingSessionLocal()
    user = User(
        username="testuser",
        password_hash=hash_password("password123"),
        role="employee",
        points_balance=1000
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user


@pytest.fixture
def test_admin():
    """创建测试管理员"""
    db = TestingSessionLocal()
    admin = User(
        username="admin",
        password_hash=hash_password("admin123"),
        role="admin",
        points_balance=0
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    db.close()
    return admin


@pytest.fixture
def auth_token(test_user):
    """创建有效的认证 token"""
    token_data = {
        "sub": str(test_user.id),
        "username": test_user.username,
        "role": test_user.role
    }
    return create_access_token(token_data)


class TestLoginEndpoint:
    """测试登录端点"""
    
    def test_login_success(self, test_user):
        """测试成功登录"""
        response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password123"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "token" in data
        assert "user" in data
        assert data["user"]["username"] == "testuser"
        assert data["user"]["role"] == "employee"
        assert data["user"]["id"] == test_user.id
    
    def test_login_wrong_password(self, test_user):
        """测试错误密码登录"""
        response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "wrongpassword"}
        )
        
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data
        assert data["detail"]["error_code"] == "AUTH001"
    
    def test_login_nonexistent_user(self):
        """测试不存在的用户登录"""
        response = client.post(
            "/api/auth/login",
            json={"username": "nonexistent", "password": "password123"}
        )
        
        assert response.status_code == 401
        data = response.json()
        assert data["detail"]["error_code"] == "AUTH001"
    
    def test_login_missing_username(self):
        """测试缺少用户名"""
        response = client.post(
            "/api/auth/login",
            json={"password": "password123"}
        )
        
        assert response.status_code == 422  # Validation error
    
    def test_login_missing_password(self):
        """测试缺少密码"""
        response = client.post(
            "/api/auth/login",
            json={"username": "testuser"}
        )
        
        assert response.status_code == 422  # Validation error
    
    def test_login_empty_username(self):
        """测试空用户名"""
        response = client.post(
            "/api/auth/login",
            json={"username": "", "password": "password123"}
        )
        
        assert response.status_code == 422  # Validation error
    
    def test_login_short_password(self):
        """测试过短密码"""
        response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "123"}
        )
        
        assert response.status_code == 422  # Validation error
    
    def test_login_admin_user(self, test_admin):
        """测试管理员登录"""
        response = client.post(
            "/api/auth/login",
            json={"username": "admin", "password": "admin123"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["user"]["role"] == "admin"


class TestLogoutEndpoint:
    """测试登出端点"""
    
    def test_logout_success(self, auth_token):
        """测试成功登出"""
        response = client.post(
            "/api/auth/logout",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Logged out successfully"
    
    def test_logout_without_token(self):
        """测试没有 token 登出"""
        response = client.post("/api/auth/logout")
        
        assert response.status_code == 401
        data = response.json()
        assert data["detail"]["error_code"] == "AUTH004"
    
    def test_logout_invalid_token(self):
        """测试无效 token 登出"""
        response = client.post(
            "/api/auth/logout",
            headers={"Authorization": "Bearer invalid_token"}
        )
        
        assert response.status_code == 401
    
    def test_logout_malformed_header(self):
        """测试格式错误的 Authorization header"""
        response = client.post(
            "/api/auth/logout",
            headers={"Authorization": "InvalidFormat token123"}
        )
        
        assert response.status_code == 401


class TestGetMeEndpoint:
    """测试获取当前用户信息端点"""
    
    def test_get_me_success(self, test_user, auth_token):
        """测试成功获取当前用户信息"""
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_user.id
        assert data["username"] == "testuser"
        assert data["role"] == "employee"
        assert data["points_balance"] == 1000
    
    def test_get_me_without_token(self):
        """测试没有 token 获取用户信息"""
        response = client.get("/api/auth/me")
        
        assert response.status_code == 401
        data = response.json()
        assert data["detail"]["error_code"] == "AUTH004"
    
    def test_get_me_invalid_token(self):
        """测试无效 token 获取用户信息"""
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": "Bearer invalid_token"}
        )
        
        assert response.status_code == 401
    
    def test_get_me_admin(self, test_admin):
        """测试管理员获取自己的信息"""
        token_data = {
            "sub": str(test_admin.id),
            "username": test_admin.username,
            "role": test_admin.role
        }
        token = create_access_token(token_data)
        
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["role"] == "admin"
        assert data["points_balance"] == 0


class TestVerifyEndpoint:
    """测试 token 验证端点"""
    
    def test_verify_valid_token(self, test_user, auth_token):
        """测试验证有效 token"""
        response = client.get(
            "/api/auth/verify",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["valid"] is True
        assert data["user_id"] == test_user.id
        assert data["role"] == "employee"
        assert data["error"] is None
    
    def test_verify_invalid_token(self):
        """测试验证无效 token"""
        response = client.get(
            "/api/auth/verify",
            headers={"Authorization": "Bearer invalid_token"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["valid"] is False
        assert data["user_id"] is None
        assert data["role"] is None
        assert "error" in data
    
    def test_verify_without_token(self):
        """测试没有 token 验证"""
        response = client.get("/api/auth/verify")
        
        assert response.status_code == 200
        data = response.json()
        assert data["valid"] is False
        assert "error" in data
    
    def test_verify_malformed_header(self):
        """测试格式错误的 header 验证"""
        response = client.get(
            "/api/auth/verify",
            headers={"Authorization": "NotBearer token123"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["valid"] is False
    
    def test_verify_admin_token(self, test_admin):
        """测试验证管理员 token"""
        token_data = {
            "sub": str(test_admin.id),
            "username": test_admin.username,
            "role": test_admin.role
        }
        token = create_access_token(token_data)
        
        response = client.get(
            "/api/auth/verify",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["valid"] is True
        assert data["role"] == "admin"


class TestHealthEndpoint:
    """测试健康检查端点"""
    
    def test_health_check(self):
        """测试健康检查"""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "database" in data


class TestRootEndpoint:
    """测试根端点"""
    
    def test_root(self):
        """测试根路径"""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "auth-service"
        assert data["version"] == "1.0.0"
        assert data["status"] == "running"


class TestAuthFlow:
    """测试完整的认证流程"""
    
    def test_full_auth_flow(self, test_user):
        """测试完整的认证流程：登录 -> 获取用户信息 -> 登出"""
        # 1. 登录
        login_response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password123"}
        )
        assert login_response.status_code == 200
        token = login_response.json()["token"]
        
        # 2. 获取用户信息
        me_response = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert me_response.status_code == 200
        assert me_response.json()["username"] == "testuser"
        
        # 3. 验证 token
        verify_response = client.get(
            "/api/auth/verify",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert verify_response.status_code == 200
        assert verify_response.json()["valid"] is True
        
        # 4. 登出
        logout_response = client.post(
            "/api/auth/logout",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert logout_response.status_code == 200
