"""Unit tests for product service."""
import pytest
from app.services.product_service import ProductService
from app.models import Product
from app.schemas import ProductCreate, ProductUpdate


class TestProductService:
    """Test cases for ProductService."""
    
    def test_create_product(self, db_session, sample_product_data):
        """Test creating a product."""
        service = ProductService()
        product_data = ProductCreate(**sample_product_data)
        
        product = service.create_product(db_session, product_data)
        
        assert product.id is not None
        assert product.name == sample_product_data["name"]
        assert product.description == sample_product_data["description"]
        assert product.points_cost == sample_product_data["points_cost"]
        assert product.is_active is True
        assert product.created_at is not None
        assert product.updated_at is not None
    
    def test_create_product_with_image(self, db_session):
        """Test creating a product with image URL."""
        service = ProductService()
        product_data = ProductCreate(
            name="Product with Image",
            description="Has an image",
            points_cost=200,
            image_url="https://example.com/image.jpg"
        )
        
        product = service.create_product(db_session, product_data)
        
        assert product.image_url == "https://example.com/image.jpg"
    
    def test_get_products_all(self, db_session):
        """Test getting all products."""
        service = ProductService()
        
        # Create test products
        service.create_product(db_session, ProductCreate(name="P1", points_cost=100))
        service.create_product(db_session, ProductCreate(name="P2", points_cost=200))
        
        products = service.get_products(db_session, is_active=None)
        
        assert len(products) == 2
    
    def test_get_products_active_only(self, db_session):
        """Test getting only active products."""
        service = ProductService()
        
        # Create products
        p1 = service.create_product(db_session, ProductCreate(name="Active", points_cost=100))
        p2 = service.create_product(db_session, ProductCreate(name="Inactive", points_cost=200))
        
        # Deactivate one
        p2.is_active = False
        db_session.commit()
        
        products = service.get_products(db_session, is_active=True)
        
        assert len(products) == 1
        assert products[0].name == "Active"
    
    def test_get_products_inactive_only(self, db_session):
        """Test getting only inactive products."""
        service = ProductService()
        
        # Create products
        p1 = service.create_product(db_session, ProductCreate(name="Active", points_cost=100))
        p2 = service.create_product(db_session, ProductCreate(name="Inactive", points_cost=200))
        
        # Deactivate one
        p2.is_active = False
        db_session.commit()
        
        products = service.get_products(db_session, is_active=False)
        
        assert len(products) == 1
        assert products[0].name == "Inactive"
    
    def test_get_product_by_id_exists(self, db_session):
        """Test getting product by ID when it exists."""
        service = ProductService()
        created = service.create_product(db_session, ProductCreate(name="Test", points_cost=100))
        
        product = service.get_product_by_id(db_session, created.id)
        
        assert product is not None
        assert product.id == created.id
        assert product.name == "Test"
    
    def test_get_product_by_id_not_exists(self, db_session):
        """Test getting product by ID when it doesn't exist."""
        service = ProductService()
        
        product = service.get_product_by_id(db_session, 999)
        
        assert product is None
    
    def test_update_product_all_fields(self, db_session):
        """Test updating all product fields."""
        service = ProductService()
        product = service.create_product(db_session, ProductCreate(name="Old", points_cost=100))
        
        update_data = ProductUpdate(
            name="New Name",
            description="New Description",
            points_cost=200,
            image_url="https://example.com/new.jpg",
            is_active=False
        )
        
        updated = service.update_product(db_session, product.id, update_data)
        
        assert updated is not None
        assert updated.name == "New Name"
        assert updated.description == "New Description"
        assert updated.points_cost == 200
        assert updated.image_url == "https://example.com/new.jpg"
        assert updated.is_active is False
    
    def test_update_product_partial_fields(self, db_session):
        """Test updating only some product fields."""
        service = ProductService()
        product = service.create_product(db_session, ProductCreate(
            name="Original",
            description="Original Desc",
            points_cost=100
        ))
        
        update_data = ProductUpdate(name="Updated Name")
        
        updated = service.update_product(db_session, product.id, update_data)
        
        assert updated is not None
        assert updated.name == "Updated Name"
        assert updated.description == "Original Desc"  # Unchanged
        assert updated.points_cost == 100  # Unchanged
    
    def test_update_product_not_exists(self, db_session):
        """Test updating non-existent product."""
        service = ProductService()
        update_data = ProductUpdate(name="New Name")
        
        result = service.update_product(db_session, 999, update_data)
        
        assert result is None
    
    def test_delete_product_exists(self, db_session):
        """Test deleting (soft delete) existing product."""
        service = ProductService()
        product = service.create_product(db_session, ProductCreate(name="To Delete", points_cost=100))
        
        result = service.delete_product(db_session, product.id)
        
        assert result is True
        
        # Verify soft delete
        deleted_product = service.get_product_by_id(db_session, product.id)
        assert deleted_product.is_active is False
    
    def test_delete_product_not_exists(self, db_session):
        """Test deleting non-existent product."""
        service = ProductService()
        
        result = service.delete_product(db_session, 999)
        
        assert result is False
    
    def test_update_product_image(self, db_session):
        """Test updating product image URL."""
        service = ProductService()
        product = service.create_product(db_session, ProductCreate(name="Test", points_cost=100))
        
        updated = service.update_product_image(db_session, product.id, "https://new-image.com/img.jpg")
        
        assert updated is not None
        assert updated.image_url == "https://new-image.com/img.jpg"
    
    def test_update_product_image_not_exists(self, db_session):
        """Test updating image for non-existent product."""
        service = ProductService()
        
        result = service.update_product_image(db_session, 999, "https://example.com/img.jpg")
        
        assert result is None
    
    def test_products_ordered_by_created_at(self, db_session):
        """Test that products are ordered by creation date (newest first)."""
        service = ProductService()
        
        p1 = service.create_product(db_session, ProductCreate(name="First", points_cost=100))
        p2 = service.create_product(db_session, ProductCreate(name="Second", points_cost=200))
        p3 = service.create_product(db_session, ProductCreate(name="Third", points_cost=300))
        
        products = service.get_products(db_session)
        
        assert products[0].name == "Third"
        assert products[1].name == "Second"
        assert products[2].name == "First"
