import pytest
from datetime import timedelta
from app.auth import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
    extract_token_from_header,
    validate_password_strength
)


class TestPasswordHashing:
    """测试密码哈希和验证功能"""
    
    def test_hash_password_returns_different_hash_each_time(self):
        """测试每次哈希密码返回不同的结果"""
        password = "testpassword123"
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        
        assert hash1 != hash2
        assert len(hash1) > 0
        assert len(hash2) > 0
    
    def test_hash_password_creates_bcrypt_hash(self):
        """测试哈希密码使用 bcrypt"""
        password = "testpassword123"
        hashed = hash_password(password)
        
        # bcrypt 哈希以 $2b$ 开头
        assert hashed.startswith("$2b$")
    
    def test_verify_password_with_correct_password(self):
        """测试使用正确密码验证"""
        password = "testpassword123"
        hashed = hash_password(password)
        
        assert verify_password(password, hashed) is True
    
    def test_verify_password_with_incorrect_password(self):
        """测试使用错误密码验证"""
        password = "testpassword123"
        wrong_password = "wrongpassword"
        hashed = hash_password(password)
        
        assert verify_password(wrong_password, hashed) is False
    
    def test_verify_password_with_empty_password(self):
        """测试使用空密码验证"""
        password = "testpassword123"
        hashed = hash_password(password)
        
        assert verify_password("", hashed) is False
    
    def test_verify_password_with_invalid_hash(self):
        """测试使用无效哈希验证"""
        password = "testpassword123"
        invalid_hash = "invalid_hash"
        
        assert verify_password(password, invalid_hash) is False


class TestJWTToken:
    """测试 JWT token 创建和解码功能"""
    
    def test_create_access_token_basic(self):
        """测试创建基本 access token"""
        data = {"sub": "123", "username": "testuser"}
        token = create_access_token(data)
        
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_create_access_token_with_custom_expiry(self):
        """测试创建带自定义过期时间的 token"""
        data = {"sub": "123", "username": "testuser"}
        expires_delta = timedelta(minutes=30)
        token = create_access_token(data, expires_delta)
        
        assert isinstance(token, str)
        payload = decode_access_token(token)
        assert payload is not None
        assert "exp" in payload
    
    def test_decode_access_token_valid(self):
        """测试解码有效 token"""
        data = {"sub": "123", "username": "testuser", "role": "employee"}
        token = create_access_token(data)
        
        payload = decode_access_token(token)
        
        assert payload is not None
        assert payload["sub"] == "123"
        assert payload["username"] == "testuser"
        assert payload["role"] == "employee"
        assert "exp" in payload
    
    def test_decode_access_token_invalid(self):
        """测试解码无效 token"""
        invalid_token = "invalid.token.string"
        
        payload = decode_access_token(invalid_token)
        
        assert payload is None
    
    def test_decode_access_token_empty(self):
        """测试解码空 token"""
        payload = decode_access_token("")
        
        assert payload is None
    
    def test_decode_access_token_malformed(self):
        """测试解码格式错误的 token"""
        malformed_token = "not-a-jwt-token"
        
        payload = decode_access_token(malformed_token)
        
        assert payload is None
    
    def test_token_contains_expiration(self):
        """测试 token 包含过期时间"""
        data = {"sub": "123"}
        token = create_access_token(data)
        payload = decode_access_token(token)
        
        assert "exp" in payload
        assert isinstance(payload["exp"], int)


class TestTokenExtraction:
    """测试从 header 提取 token 功能"""
    
    def test_extract_token_valid_bearer(self):
        """测试从有效 Bearer header 提取 token"""
        auth_header = "Bearer abc123xyz"
        token = extract_token_from_header(auth_header)
        
        assert token == "abc123xyz"
    
    def test_extract_token_case_insensitive(self):
        """测试 Bearer 关键字大小写不敏感"""
        auth_header = "bearer abc123xyz"
        token = extract_token_from_header(auth_header)
        
        assert token == "abc123xyz"
    
    def test_extract_token_none_header(self):
        """测试 None header"""
        token = extract_token_from_header(None)
        
        assert token is None
    
    def test_extract_token_empty_header(self):
        """测试空 header"""
        token = extract_token_from_header("")
        
        assert token is None
    
    def test_extract_token_invalid_format(self):
        """测试无效格式的 header"""
        auth_header = "InvalidFormat abc123"
        token = extract_token_from_header(auth_header)
        
        assert token is None
    
    def test_extract_token_missing_token(self):
        """测试只有 Bearer 没有 token"""
        auth_header = "Bearer"
        token = extract_token_from_header(auth_header)
        
        assert token is None
    
    def test_extract_token_with_extra_spaces(self):
        """测试 Bearer 和 token 之间有多个空格"""
        auth_header = "Bearer   abc123"
        token = extract_token_from_header(auth_header)
        
        # 应该返回 None，因为格式不正确（多个空格会被 split 分成多个部分）
        assert token is None or token == ""


class TestPasswordValidation:
    """测试密码强度验证功能"""
    
    def test_validate_password_strength_valid(self):
        """测试有效密码（满足最小长度）"""
        password = "password123"
        assert validate_password_strength(password) is True
    
    def test_validate_password_strength_minimum_length(self):
        """测试最小长度密码"""
        password = "12345678"  # 8 字符
        assert validate_password_strength(password) is True
    
    def test_validate_password_strength_too_short(self):
        """测试过短密码"""
        password = "1234567"  # 7 字符
        assert validate_password_strength(password) is False
    
    def test_validate_password_strength_empty(self):
        """测试空密码"""
        password = ""
        assert validate_password_strength(password) is False
    
    def test_validate_password_strength_long(self):
        """测试长密码"""
        password = "a" * 100
        assert validate_password_strength(password) is True


class TestAuthIntegration:
    """测试认证模块的集成功能"""
    
    def test_full_password_flow(self):
        """测试完整的密码流程：哈希 -> 验证"""
        password = "mypassword123"
        
        # 哈希密码
        hashed = hash_password(password)
        
        # 验证正确密码
        assert verify_password(password, hashed) is True
        
        # 验证错误密码
        assert verify_password("wrongpassword", hashed) is False
    
    def test_full_token_flow(self):
        """测试完整的 token 流程：创建 -> 提取 -> 解码"""
        # 创建 token
        data = {"sub": "456", "username": "john", "role": "admin"}
        token = create_access_token(data)
        
        # 模拟 Authorization header
        auth_header = f"Bearer {token}"
        
        # 提取 token
        extracted_token = extract_token_from_header(auth_header)
        assert extracted_token == token
        
        # 解码 token
        payload = decode_access_token(extracted_token)
        assert payload is not None
        assert payload["sub"] == "456"
        assert payload["username"] == "john"
        assert payload["role"] == "admin"
