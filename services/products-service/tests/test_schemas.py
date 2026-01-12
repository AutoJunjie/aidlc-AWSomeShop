"""Unit tests for Pydantic schemas."""
import pytest
from pydantic import ValidationError
from app.schemas import (
    ProductCreate, ProductUpdate, ProductResponse,
    ImageUploadResponse, ErrorResponse, HealthCheckResponse
)
from datetime import datetime


class TestProductSchemas:
    """Test cases for product schemas."""
    
    def test_product_create_valid(self):
        """Test creating valid ProductCreate schema."""
        data = {
            "name": "Test Product",
            "description": "Test Description",
            "points_cost": 100
        }
        product = ProductCreate(**data)
        
        assert product.name == "Test Product"
        assert product.description == "Test Description"
        assert product.points_cost == 100
    
    def test_product_create_with_image_url(self):
        """Test ProductCreate with image URL."""
        data = {
            "name": "Product",
            "points_cost": 100,
            "image_url": "https://example.com/image.jpg"
        }
        product = ProductCreate(**data)
        
        assert product.image_url == "https://example.com/image.jpg"
    
    def test_product_create_missing_name(self):
        """Test ProductCreate with missing name."""
        data = {
            "description": "Test",
            "points_cost": 100
        }
        
        with pytest.raises(ValidationError) as exc_info:
            ProductCreate(**data)
        
        assert "name" in str(exc_info.value)
    
    def test_product_create_missing_points_cost(self):
        """Test ProductCreate with missing points_cost."""
        data = {
            "name": "Test Product",
            "description": "Test"
        }
        
        with pytest.raises(ValidationError) as exc_info:
            ProductCreate(**data)
        
        assert "points_cost" in str(exc_info.value)
    
    def test_product_create_negative_points(self):
        """Test ProductCreate with negative points cost."""
        data = {
            "name": "Test",
            "points_cost": -10
        }
        
        with pytest.raises(ValidationError) as exc_info:
            ProductCreate(**data)
        
        assert "points_cost" in str(exc_info.value)
    
    def test_product_create_zero_points(self):
        """Test ProductCreate with zero points cost."""
        data = {
            "name": "Test",
            "points_cost": 0
        }
        
        with pytest.raises(ValidationError) as exc_info:
            ProductCreate(**data)
        
        assert "points_cost" in str(exc_info.value)
    
    def test_product_create_name_too_long(self):
        """Test ProductCreate with name exceeding max length."""
        data = {
            "name": "x" * 101,  # Max is 100
            "points_cost": 100
        }
        
        with pytest.raises(ValidationError) as exc_info:
            ProductCreate(**data)
        
        assert "name" in str(exc_info.value)
    
    def test_product_create_name_empty(self):
        """Test ProductCreate with empty name."""
        data = {
            "name": "",
            "points_cost": 100
        }
        
        with pytest.raises(ValidationError) as exc_info:
            ProductCreate(**data)
        
        assert "name" in str(exc_info.value)
    
    def test_product_create_description_too_long(self):
        """Test ProductCreate with description exceeding max length."""
        data = {
            "name": "Test",
            "description": "x" * 1001,  # Max is 1000
            "points_cost": 100
        }
        
        with pytest.raises(ValidationError) as exc_info:
            ProductCreate(**data)
        
        assert "description" in str(exc_info.value)
    
    def test_product_update_all_fields(self):
        """Test ProductUpdate with all fields."""
        data = {
            "name": "Updated",
            "description": "Updated desc",
            "points_cost": 200,
            "image_url": "https://new.com/img.jpg",
            "is_active": False
        }
        product = ProductUpdate(**data)
        
        assert product.name == "Updated"
        assert product.description == "Updated desc"
        assert product.points_cost == 200
        assert product.image_url == "https://new.com/img.jpg"
        assert product.is_active is False
    
    def test_product_update_partial_fields(self):
        """Test ProductUpdate with only some fields."""
        data = {"name": "New Name"}
        product = ProductUpdate(**data)
        
        assert product.name == "New Name"
        assert product.description is None
        assert product.points_cost is None
    
    def test_product_update_empty(self):
        """Test ProductUpdate with no fields."""
        product = ProductUpdate()
        
        assert product.name is None
        assert product.description is None
        assert product.points_cost is None
        assert product.image_url is None
        assert product.is_active is None
    
    def test_product_update_invalid_points(self):
        """Test ProductUpdate with invalid points."""
        data = {"points_cost": -5}
        
        with pytest.raises(ValidationError):
            ProductUpdate(**data)
    
    def test_image_upload_response(self):
        """Test ImageUploadResponse schema."""
        data = {"image_url": "https://s3.example.com/image.jpg"}
        response = ImageUploadResponse(**data)
        
        assert response.image_url == "https://s3.example.com/image.jpg"
    
    def test_error_response_with_detail(self):
        """Test ErrorResponse with detail."""
        data = {
            "error": "PRODUCT_NOT_FOUND",
            "detail": "Product with ID 123 not found"
        }
        response = ErrorResponse(**data)
        
        assert response.error == "PRODUCT_NOT_FOUND"
        assert response.detail == "Product with ID 123 not found"
    
    def test_error_response_without_detail(self):
        """Test ErrorResponse without detail."""
        data = {"error": "UNAUTHORIZED"}
        response = ErrorResponse(**data)
        
        assert response.error == "UNAUTHORIZED"
        assert response.detail is None
    
    def test_health_check_response(self):
        """Test HealthCheckResponse schema."""
        data = {
            "status": "healthy",
            "database": True,
            "s3": True
        }
        response = HealthCheckResponse(**data)
        
        assert response.status == "healthy"
        assert response.database is True
        assert response.s3 is True
    
    def test_health_check_response_unhealthy(self):
        """Test HealthCheckResponse for unhealthy state."""
        data = {
            "status": "unhealthy",
            "database": False,
            "s3": False
        }
        response = HealthCheckResponse(**data)
        
        assert response.status == "unhealthy"
        assert response.database is False
        assert response.s3 is False
