"""Unit tests for internal API routes."""
import pytest
from app.schemas import ProductCreate


class TestInternalRoutes:
    """Test cases for internal API routes."""
    
    def test_get_product_internal_success(self, client, db_session, sample_product_data):
        """Test getting product via internal API."""
        from app.services.product_service import product_service
        
        product = product_service.create_product(db_session, ProductCreate(**sample_product_data))
        
        response = client.get(f"/internal/products/{product.id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == product.id
        assert data["name"] == sample_product_data["name"]
    
    def test_get_product_internal_not_found(self, client):
        """Test getting non-existent product via internal API."""
        response = client.get("/internal/products/999")
        
        assert response.status_code == 404
        assert "PRODUCT_NOT_FOUND" in response.json()["detail"]
    
    def test_internal_api_no_auth_required(self, client, db_session, sample_product_data):
        """Test that internal API does not require authentication."""
        from app.services.product_service import product_service
        
        product = product_service.create_product(db_session, ProductCreate(**sample_product_data))
        
        # Call without any authentication headers
        response = client.get(f"/internal/products/{product.id}")
        
        # Should succeed without auth
        assert response.status_code == 200
