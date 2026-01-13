"""Tests for security functions (password hashing and JWT)"""
import pytest
from app.security import hash_password, verify_password, create_access_token, decode_access_token
from datetime import datetime, timedelta


def test_hash_password():
    """Test password hashing"""
    password = "TestPassword123"
    hashed = hash_password(password)
    
    assert hashed != password
    assert hashed.startswith("$2b$")
    assert len(hashed) > 50


def test_verify_password_correct():
    """Test password verification with correct password"""
    password = "TestPassword123"
    hashed = hash_password(password)
    
    assert verify_password(password, hashed) is True


def test_verify_password_incorrect():
    """Test password verification with incorrect password"""
    password = "TestPassword123"
    hashed = hash_password(password)
    
    assert verify_password("WrongPassword", hashed) is False


def test_verify_password_case_sensitive():
    """Test that password verification is case sensitive"""
    password = "TestPassword123"
    hashed = hash_password(password)
    
    assert verify_password("testpassword123", hashed) is False


def test_create_access_token():
    """Test JWT token creation"""
    data = {
        "user_id": 1,
        "username": "testuser",
        "role": "employee"
    }
    
    token = create_access_token(data)
    
    assert isinstance(token, str)
    assert len(token) > 0
    assert token.count('.') == 2


def test_decode_access_token_valid():
    """Test decoding valid JWT token"""
    data = {
        "user_id": 1,
        "username": "testuser",
        "role": "employee"
    }
    
    token = create_access_token(data)
    decoded = decode_access_token(token)
    
    assert decoded is not None
    assert decoded["user_id"] == 1
    assert decoded["username"] == "testuser"
    assert decoded["role"] == "employee"
    assert "exp" in decoded
    assert "iat" in decoded


def test_decode_access_token_invalid():
    """Test decoding invalid JWT token"""
    invalid_token = "invalid.token.here"
    
    decoded = decode_access_token(invalid_token)
    
    assert decoded is None


def test_decode_access_token_malformed():
    """Test decoding malformed JWT token"""
    malformed_token = "not-a-jwt-token"
    
    decoded = decode_access_token(malformed_token)
    
    assert decoded is None


def test_token_expiration_field():
    """Test that token contains expiration field"""
    data = {
        "user_id": 1,
        "username": "testuser",
        "role": "employee"
    }
    
    token = create_access_token(data)
    decoded = decode_access_token(token)
    
    assert "exp" in decoded
    exp_timestamp = decoded["exp"]
    iat_timestamp = decoded["iat"]
    
    exp_time = datetime.fromtimestamp(exp_timestamp)
    iat_time = datetime.fromtimestamp(iat_timestamp)
    
    time_diff = exp_time - iat_time
    assert abs(time_diff.total_seconds() - 24 * 3600) < 10


def test_hash_password_different_salts():
    """Test that same password produces different hashes (different salts)"""
    password = "TestPassword123"
    hash1 = hash_password(password)
    hash2 = hash_password(password)
    
    assert hash1 != hash2
    assert verify_password(password, hash1)
    assert verify_password(password, hash2)
