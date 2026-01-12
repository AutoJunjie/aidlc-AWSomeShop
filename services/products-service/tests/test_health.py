"""Unit tests for health check route."""
import pytest
from unittest.mock import patch


class TestHealthCheck:
    """Test cases for health check endpoint."""
    
    @patch('app.routes.health.check_db_connection')
    @patch('app.routes.health.s3_service.check_connection')
    def test_health_check_all_healthy(self, mock_s3_check, mock_db_check, client):
        """Test health check when all services are healthy."""
        mock_db_check.return_value = True
        mock_s3_check.return_value = True
        
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["database"] is True
        assert data["s3"] is True
    
    @patch('app.routes.health.check_db_connection')
    @patch('app.routes.health.s3_service.check_connection')
    def test_health_check_db_unhealthy(self, mock_s3_check, mock_db_check, client):
        """Test health check when database is unhealthy."""
        mock_db_check.return_value = False
        mock_s3_check.return_value = True
        
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "unhealthy"
        assert data["database"] is False
        assert data["s3"] is True
    
    @patch('app.routes.health.check_db_connection')
    @patch('app.routes.health.s3_service.check_connection')
    def test_health_check_s3_unhealthy(self, mock_s3_check, mock_db_check, client):
        """Test health check when S3 is unhealthy."""
        mock_db_check.return_value = True
        mock_s3_check.return_value = False
        
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "unhealthy"
        assert data["database"] is True
        assert data["s3"] is False
    
    @patch('app.routes.health.check_db_connection')
    @patch('app.routes.health.s3_service.check_connection')
    def test_health_check_all_unhealthy(self, mock_s3_check, mock_db_check, client):
        """Test health check when all services are unhealthy."""
        mock_db_check.return_value = False
        mock_s3_check.return_value = False
        
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "unhealthy"
        assert data["database"] is False
        assert data["s3"] is False
