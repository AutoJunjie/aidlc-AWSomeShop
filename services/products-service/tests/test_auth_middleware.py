"""Unit tests for authentication middleware."""
import pytest
from unittest.mock import Mock, patch
from app.middleware.auth import (
    verify_token, verify_admin, 
    AuthenticationError, AuthorizationError
)
import requests


class TestAuthMiddleware:
    """Test cases for authentication middleware."""
    
    def test_verify_token_missing_header(self):
        """Test token verification with missing authorization header."""
        with pytest.raises(AuthenticationError) as exc_info:
            verify_token(None)
        
        assert "Missing authorization header" in str(exc_info.value.detail)
    
    def test_verify_token_invalid_format(self):
        """Test token verification with invalid header format."""
        with pytest.raises(AuthenticationError) as exc_info:
            verify_token("InvalidFormat token123")
        
        assert "Invalid authorization header format" in str(exc_info.value.detail)
    
    @patch('app.middleware.auth.requests.get')
    def test_verify_token_success(self, mock_get):
        """Test successful token verification."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "user_id": 1,
            "username": "testuser",
            "role": "user"
        }
        mock_get.return_value = mock_response
        
        result = verify_token("Bearer valid_token")
        
        assert result["user_id"] == 1
        assert result["username"] == "testuser"
        assert result["role"] == "user"
        
        # Verify the auth service was called correctly
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert "Authorization" in call_args[1]["headers"]
        assert call_args[1]["headers"]["Authorization"] == "Bearer valid_token"
    
    @patch('app.middleware.auth.requests.get')
    def test_verify_token_unauthorized(self, mock_get):
        """Test token verification with invalid token."""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_get.return_value = mock_response
        
        with pytest.raises(AuthenticationError) as exc_info:
            verify_token("Bearer invalid_token")
        
        assert "Invalid or expired token" in str(exc_info.value.detail)
    
    @patch('app.middleware.auth.requests.get')
    def test_verify_token_auth_service_error(self, mock_get):
        """Test token verification when auth service returns error."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response
        
        with pytest.raises(AuthenticationError) as exc_info:
            verify_token("Bearer token123")
        
        assert "Authentication failed" in str(exc_info.value.detail)
    
    @patch('app.middleware.auth.requests.get')
    def test_verify_token_connection_error(self, mock_get):
        """Test token verification when auth service is unavailable."""
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection refused")
        
        with pytest.raises(AuthenticationError) as exc_info:
            verify_token("Bearer token123")
        
        assert "Authentication service unavailable" in str(exc_info.value.detail)
    
    @patch('app.middleware.auth.requests.get')
    def test_verify_token_timeout(self, mock_get):
        """Test token verification with timeout."""
        mock_get.side_effect = requests.exceptions.Timeout("Timeout")
        
        with pytest.raises(AuthenticationError) as exc_info:
            verify_token("Bearer token123")
        
        assert "Authentication service unavailable" in str(exc_info.value.detail)
    
    @patch('app.middleware.auth.verify_token')
    def test_verify_admin_success(self, mock_verify_token):
        """Test successful admin verification."""
        mock_verify_token.return_value = {
            "user_id": 2,
            "username": "admin",
            "role": "admin"
        }
        
        result = verify_admin("Bearer admin_token")
        
        assert result["user_id"] == 2
        assert result["role"] == "admin"
    
    @patch('app.middleware.auth.verify_token')
    def test_verify_admin_not_admin(self, mock_verify_token):
        """Test admin verification when user is not admin."""
        mock_verify_token.return_value = {
            "user_id": 1,
            "username": "normaluser",
            "role": "user"
        }
        
        with pytest.raises(AuthorizationError) as exc_info:
            verify_admin("Bearer user_token")
        
        assert "Admin privileges required" in str(exc_info.value.detail)
    
    @patch('app.middleware.auth.verify_token')
    def test_verify_admin_missing_role(self, mock_verify_token):
        """Test admin verification when role is missing."""
        mock_verify_token.return_value = {
            "user_id": 1,
            "username": "user"
        }
        
        with pytest.raises(AuthorizationError):
            verify_admin("Bearer user_token")
    
    def test_authentication_error_status_code(self):
        """Test AuthenticationError has correct status code."""
        error = AuthenticationError("Test error")
        
        assert error.status_code == 401
        assert error.detail == "Test error"
    
    def test_authorization_error_status_code(self):
        """Test AuthorizationError has correct status code."""
        error = AuthorizationError("Test error")
        
        assert error.status_code == 403
        assert error.detail == "Test error"
    
    def test_authorization_error_default_message(self):
        """Test AuthorizationError default message."""
        error = AuthorizationError()
        
        assert error.detail == "Insufficient permissions"
