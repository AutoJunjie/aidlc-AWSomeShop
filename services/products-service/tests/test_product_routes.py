"""Unit tests for product API routes."""
import pytest
from unittest.mock import patch, Mock
from io import BytesIO


class TestProductRoutes:
    """Test cases for product API routes."""
    
    @patch('app.routes.products.get_current_user')
    def test_get_products_success(self, mock_auth, client, db_session, sample_product_data):
        """Test getting product list."""
        mock_auth.return_value = {"user_id": 1, "role": "user"}
        
        # Create test products
        from app.services.product_service import product_service
        from app.schemas import ProductCreate
        product_service.create_product(db_session, ProductCreate(**sample_product_data))
        
        response = client.get("/api/products")
        
        assert response.status_code == 200
        data = response.json()
        assert "products" in data
        assert len(data["products"]) == 1
    
    @patch('app.routes.products.get_current_user')
    def test_get_products_filter_active(self, mock_auth, client, db_session):
        """Test getting products filtered by active status."""
        mock_auth.return_value = {"user_id": 1, "role": "user"}
        
        from app.services.product_service import product_service
        from app.schemas import ProductCreate
        
        # Create active and inactive products
        p1 = product_service.create_product(db_session, ProductCreate(name="Active", points_cost=100))
        p2 = product_service.create_product(db_session, ProductCreate(name="Inactive", points_cost=200))
        product_service.delete_product(db_session, p2.id)
        
        response = client.get("/api/products?is_active=true")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["products"]) == 1
        assert data["products"][0]["name"] == "Active"
    
    def test_get_products_unauthorized(self, client):
        """Test getting products without authentication."""
        response = client.get("/api/products")
        
        assert response.status_code == 401
    
    @patch('app.routes.products.get_current_user')
    def test_get_product_by_id_success(self, mock_auth, client, db_session, sample_product_data):
        """Test getting product by ID."""
        mock_auth.return_value = {"user_id": 1, "role": "user"}
        
        from app.services.product_service import product_service
        from app.schemas import ProductCreate
        product = product_service.create_product(db_session, ProductCreate(**sample_product_data))
        
        response = client.get(f"/api/products/{product.id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == product.id
        assert data["name"] == sample_product_data["name"]
    
    @patch('app.routes.products.get_current_user')
    def test_get_product_by_id_not_found(self, mock_auth, client):
        """Test getting non-existent product."""
        mock_auth.return_value = {"user_id": 1, "role": "user"}
        
        response = client.get("/api/products/999")
        
        assert response.status_code == 404
        assert "PRODUCT_NOT_FOUND" in response.json()["detail"]
    
    @patch('app.routes.products.get_admin_user')
    def test_create_product_success(self, mock_auth, client, sample_product_data):
        """Test creating a product as admin."""
        mock_auth.return_value = {"user_id": 2, "role": "admin"}
        
        response = client.post("/api/products", json=sample_product_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == sample_product_data["name"]
        assert data["points_cost"] == sample_product_data["points_cost"]
        assert "id" in data
    
    @patch('app.routes.products.get_admin_user')
    def test_create_product_invalid_points(self, mock_auth, client):
        """Test creating product with invalid points cost."""
        mock_auth.return_value = {"user_id": 2, "role": "admin"}
        
        response = client.post("/api/products", json={
            "name": "Test",
            "points_cost": -10  # Invalid: negative
        })
        
        assert response.status_code == 422  # Validation error
    
    @patch('app.routes.products.get_admin_user')
    def test_create_product_missing_required_fields(self, mock_auth, client):
        """Test creating product with missing required fields."""
        mock_auth.return_value = {"user_id": 2, "role": "admin"}
        
        response = client.post("/api/products", json={
            "description": "Missing name and points_cost"
        })
        
        assert response.status_code == 422
    
    def test_create_product_unauthorized(self, client, sample_product_data):
        """Test creating product without authentication."""
        response = client.post("/api/products", json=sample_product_data)
        
        assert response.status_code == 401
    
    @patch('app.routes.products.get_current_user')
    def test_create_product_forbidden(self, mock_auth, client, sample_product_data):
        """Test creating product as non-admin user."""
        mock_auth.return_value = {"user_id": 1, "role": "user"}
        
        # This will fail at the get_admin_user dependency
        response = client.post("/api/products", json=sample_product_data)
        
        # Should fail before reaching the route since get_admin_user is required
        assert response.status_code in [401, 403]
    
    @patch('app.routes.products.get_admin_user')
    def test_update_product_success(self, mock_auth, client, db_session, sample_product_data):
        """Test updating a product."""
        mock_auth.return_value = {"user_id": 2, "role": "admin"}
        
        from app.services.product_service import product_service
        from app.schemas import ProductCreate
        product = product_service.create_product(db_session, ProductCreate(**sample_product_data))
        
        update_data = {"name": "Updated Name", "points_cost": 200}
        response = client.put(f"/api/products/{product.id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Name"
        assert data["points_cost"] == 200
    
    @patch('app.routes.products.get_admin_user')
    def test_update_product_not_found(self, mock_auth, client):
        """Test updating non-existent product."""
        mock_auth.return_value = {"user_id": 2, "role": "admin"}
        
        response = client.put("/api/products/999", json={"name": "New Name"})
        
        assert response.status_code == 404
    
    @patch('app.routes.products.get_admin_user')
    def test_delete_product_success(self, mock_auth, client, db_session, sample_product_data):
        """Test deleting a product."""
        mock_auth.return_value = {"user_id": 2, "role": "admin"}
        
        from app.services.product_service import product_service
        from app.schemas import ProductCreate
        product = product_service.create_product(db_session, ProductCreate(**sample_product_data))
        
        response = client.delete(f"/api/products/{product.id}")
        
        assert response.status_code == 204
        
        # Verify soft delete
        deleted = product_service.get_product_by_id(db_session, product.id)
        assert deleted.is_active is False
    
    @patch('app.routes.products.get_admin_user')
    def test_delete_product_not_found(self, mock_auth, client):
        """Test deleting non-existent product."""
        mock_auth.return_value = {"user_id": 2, "role": "admin"}
        
        response = client.delete("/api/products/999")
        
        assert response.status_code == 404
    
    @patch('app.routes.products.get_admin_user')
    @patch('app.routes.products.s3_service')
    def test_upload_image_success(self, mock_s3, mock_auth, client, db_session, sample_product_data):
        """Test uploading product image."""
        mock_auth.return_value = {"user_id": 2, "role": "admin"}
        mock_s3.upload_file.return_value = "https://s3.example.com/products/1/test.jpg"
        
        from app.services.product_service import product_service
        from app.schemas import ProductCreate
        product = product_service.create_product(db_session, ProductCreate(**sample_product_data))
        
        # Create fake image file
        file_content = b"fake image content"
        files = {"file": ("test.jpg", BytesIO(file_content), "image/jpeg")}
        
        response = client.post(f"/api/products/{product.id}/image", files=files)
        
        assert response.status_code == 200
        data = response.json()
        assert "image_url" in data
        assert data["image_url"] == "https://s3.example.com/products/1/test.jpg"
    
    @patch('app.routes.products.get_admin_user')
    def test_upload_image_product_not_found(self, mock_auth, client):
        """Test uploading image for non-existent product."""
        mock_auth.return_value = {"user_id": 2, "role": "admin"}
        
        files = {"file": ("test.jpg", BytesIO(b"content"), "image/jpeg")}
        response = client.post("/api/products/999/image", files=files)
        
        assert response.status_code == 404
    
    @patch('app.routes.products.get_admin_user')
    def test_upload_image_invalid_file_type(self, mock_auth, client, db_session, sample_product_data):
        """Test uploading image with invalid file type."""
        mock_auth.return_value = {"user_id": 2, "role": "admin"}
        
        from app.services.product_service import product_service
        from app.schemas import ProductCreate
        product = product_service.create_product(db_session, ProductCreate(**sample_product_data))
        
        files = {"file": ("test.txt", BytesIO(b"content"), "text/plain")}
        response = client.post(f"/api/products/{product.id}/image", files=files)
        
        assert response.status_code == 400
        assert "INVALID_FILE_TYPE" in response.json()["detail"]
    
    @patch('app.routes.products.get_admin_user')
    def test_upload_image_file_too_large(self, mock_auth, client, db_session, sample_product_data):
        """Test uploading image that exceeds size limit."""
        mock_auth.return_value = {"user_id": 2, "role": "admin"}
        
        from app.services.product_service import product_service
        from app.schemas import ProductCreate
        product = product_service.create_product(db_session, ProductCreate(**sample_product_data))
        
        # Create file larger than 5MB
        large_content = b"x" * (6 * 1024 * 1024)
        files = {"file": ("test.jpg", BytesIO(large_content), "image/jpeg")}
        
        response = client.post(f"/api/products/{product.id}/image", files=files)
        
        assert response.status_code == 400
        assert "FILE_TOO_LARGE" in response.json()["detail"]
