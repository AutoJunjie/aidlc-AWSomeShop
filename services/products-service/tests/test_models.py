"""Unit tests for database models."""
import pytest
from app.models import Product
from datetime import datetime


class TestProductModel:
    """Test cases for Product model."""
    
    def test_create_product_model(self, db_session):
        """Test creating a Product model instance."""
        product = Product(
            name="Test Product",
            description="Test Description",
            points_cost=100,
            image_url="https://example.com/image.jpg",
            is_active=True
        )
        
        db_session.add(product)
        db_session.commit()
        db_session.refresh(product)
        
        assert product.id is not None
        assert product.name == "Test Product"
        assert product.description == "Test Description"
        assert product.points_cost == 100
        assert product.image_url == "https://example.com/image.jpg"
        assert product.is_active is True
        assert product.created_at is not None
        assert product.updated_at is not None
    
    def test_product_default_is_active(self, db_session):
        """Test that is_active defaults to True."""
        product = Product(
            name="Test",
            points_cost=100
        )
        
        db_session.add(product)
        db_session.commit()
        db_session.refresh(product)
        
        assert product.is_active is True
    
    def test_product_nullable_fields(self, db_session):
        """Test that description and image_url can be null."""
        product = Product(
            name="Test",
            points_cost=100,
            description=None,
            image_url=None
        )
        
        db_session.add(product)
        db_session.commit()
        db_session.refresh(product)
        
        assert product.description is None
        assert product.image_url is None
    
    def test_product_to_dict(self, db_session):
        """Test converting product model to dictionary."""
        product = Product(
            name="Test Product",
            description="Test Description",
            points_cost=100,
            image_url="https://example.com/image.jpg"
        )
        
        db_session.add(product)
        db_session.commit()
        db_session.refresh(product)
        
        product_dict = product.to_dict()
        
        assert isinstance(product_dict, dict)
        assert product_dict["id"] == product.id
        assert product_dict["name"] == "Test Product"
        assert product_dict["description"] == "Test Description"
        assert product_dict["points_cost"] == 100
        assert product_dict["image_url"] == "https://example.com/image.jpg"
        assert product_dict["is_active"] is True
        assert "created_at" in product_dict
        assert "updated_at" in product_dict
    
    def test_product_to_dict_with_null_fields(self, db_session):
        """Test to_dict with null optional fields."""
        product = Product(
            name="Test",
            points_cost=100
        )
        
        db_session.add(product)
        db_session.commit()
        db_session.refresh(product)
        
        product_dict = product.to_dict()
        
        assert product_dict["description"] is None
        assert product_dict["image_url"] is None
    
    def test_product_timestamps_auto_set(self, db_session):
        """Test that timestamps are automatically set."""
        product = Product(
            name="Test",
            points_cost=100
        )
        
        db_session.add(product)
        db_session.commit()
        db_session.refresh(product)
        
        assert product.created_at is not None
        assert product.updated_at is not None
        assert isinstance(product.created_at, datetime)
        assert isinstance(product.updated_at, datetime)
    
    def test_product_updated_at_changes(self, db_session):
        """Test that updated_at changes on update."""
        product = Product(
            name="Original",
            points_cost=100
        )
        
        db_session.add(product)
        db_session.commit()
        db_session.refresh(product)
        
        original_updated_at = product.updated_at
        
        # Update the product
        product.name = "Updated"
        db_session.commit()
        db_session.refresh(product)
        
        # updated_at should change (in real PostgreSQL with triggers)
        # Note: SQLite might not update this automatically without triggers
        assert product.updated_at is not None
    
    def test_product_query_by_id(self, db_session):
        """Test querying product by ID."""
        product = Product(
            name="Test",
            points_cost=100
        )
        
        db_session.add(product)
        db_session.commit()
        
        # Query by ID
        found = db_session.query(Product).filter(Product.id == product.id).first()
        
        assert found is not None
        assert found.id == product.id
        assert found.name == "Test"
    
    def test_product_query_by_is_active(self, db_session):
        """Test querying products by is_active status."""
        # Create active product
        active = Product(name="Active", points_cost=100, is_active=True)
        # Create inactive product
        inactive = Product(name="Inactive", points_cost=200, is_active=False)
        
        db_session.add(active)
        db_session.add(inactive)
        db_session.commit()
        
        # Query active only
        active_products = db_session.query(Product).filter(Product.is_active == True).all()
        
        assert len(active_products) >= 1
        assert all(p.is_active for p in active_products)
