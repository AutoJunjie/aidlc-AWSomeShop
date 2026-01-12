"""Product service - business logic layer."""
from sqlalchemy.orm import Session
from app.models import Product
from app.schemas import ProductCreate, ProductUpdate
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


class ProductService:
    """Service for product business logic."""
    
    def get_products(self, db: Session, is_active: Optional[bool] = None) -> List[Product]:
        """
        Get list of products.
        
        Args:
            db: Database session
            is_active: Filter by active status (None = all products)
        
        Returns:
            List[Product]: List of products
        """
        query = db.query(Product)
        
        if is_active is not None:
            query = query.filter(Product.is_active == is_active)
        
        products = query.order_by(Product.created_at.desc()).all()
        logger.info(f"Retrieved {len(products)} products (is_active={is_active})")
        return products
    
    def get_product_by_id(self, db: Session, product_id: int) -> Optional[Product]:
        """
        Get product by ID.
        
        Args:
            db: Database session
            product_id: Product ID
        
        Returns:
            Optional[Product]: Product if found, None otherwise
        """
        product = db.query(Product).filter(Product.id == product_id).first()
        if product:
            logger.info(f"Retrieved product {product_id}")
        else:
            logger.warning(f"Product {product_id} not found")
        return product
    
    def create_product(self, db: Session, product_data: ProductCreate) -> Product:
        """
        Create new product.
        
        Args:
            db: Database session
            product_data: Product creation data
        
        Returns:
            Product: Created product
        """
        product = Product(
            name=product_data.name,
            description=product_data.description,
            points_cost=product_data.points_cost,
            image_url=product_data.image_url,
            is_active=True
        )
        
        db.add(product)
        db.commit()
        db.refresh(product)
        
        logger.info(f"Created product {product.id}: {product.name}")
        return product
    
    def update_product(self, db: Session, product_id: int, product_data: ProductUpdate) -> Optional[Product]:
        """
        Update product.
        
        Args:
            db: Database session
            product_id: Product ID
            product_data: Product update data
        
        Returns:
            Optional[Product]: Updated product if found, None otherwise
        """
        product = self.get_product_by_id(db, product_id)
        if not product:
            return None
        
        # Update fields if provided
        update_data = product_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(product, field, value)
        
        db.commit()
        db.refresh(product)
        
        logger.info(f"Updated product {product_id}")
        return product
    
    def delete_product(self, db: Session, product_id: int) -> bool:
        """
        Delete product (soft delete - set is_active to False).
        
        Args:
            db: Database session
            product_id: Product ID
        
        Returns:
            bool: True if successful, False if product not found
        """
        product = self.get_product_by_id(db, product_id)
        if not product:
            return False
        
        product.is_active = False
        db.commit()
        
        logger.info(f"Deleted (soft) product {product_id}")
        return True
    
    def update_product_image(self, db: Session, product_id: int, image_url: str) -> Optional[Product]:
        """
        Update product image URL.
        
        Args:
            db: Database session
            product_id: Product ID
            image_url: New image URL
        
        Returns:
            Optional[Product]: Updated product if found, None otherwise
        """
        product = self.get_product_by_id(db, product_id)
        if not product:
            return None
        
        product.image_url = image_url
        db.commit()
        db.refresh(product)
        
        logger.info(f"Updated image for product {product_id}")
        return product


# Create singleton instance
product_service = ProductService()
