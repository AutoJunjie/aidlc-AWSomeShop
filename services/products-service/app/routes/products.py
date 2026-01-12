"""API routes for products."""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import (
    ProductCreate, ProductUpdate, ProductResponse, 
    ProductListResponse, ImageUploadResponse, ErrorResponse
)
from app.services.product_service import product_service
from app.services.s3_service import s3_service
from app.middleware.auth import get_current_user, get_admin_user
from app.config import settings
import logging
from typing import Optional

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/products", tags=["products"])


@router.get("", response_model=ProductListResponse)
async def get_products(
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Get list of products.
    Requires authentication.
    """
    try:
        products = product_service.get_products(db, is_active)
        return ProductListResponse(
            products=[ProductResponse.model_validate(p) for p in products]
        )
    except Exception as e:
        logger.error(f"Error getting products: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve products"
        )


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Get product by ID.
    Requires authentication.
    """
    product = product_service.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="PRODUCT_NOT_FOUND"
        )
    return ProductResponse.model_validate(product)


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    admin: dict = Depends(get_admin_user)
):
    """
    Create new product.
    Requires admin privileges.
    """
    try:
        product = product_service.create_product(db, product_data)
        logger.info(f"Admin {admin.get('user_id')} created product {product.id}")
        return ProductResponse.model_validate(product)
    except Exception as e:
        logger.error(f"Error creating product: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create product"
        )


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    admin: dict = Depends(get_admin_user)
):
    """
    Update product.
    Requires admin privileges.
    """
    product = product_service.update_product(db, product_id, product_data)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="PRODUCT_NOT_FOUND"
        )
    logger.info(f"Admin {admin.get('user_id')} updated product {product_id}")
    return ProductResponse.model_validate(product)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    admin: dict = Depends(get_admin_user)
):
    """
    Delete product (soft delete).
    Requires admin privileges.
    """
    success = product_service.delete_product(db, product_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="PRODUCT_NOT_FOUND"
        )
    logger.info(f"Admin {admin.get('user_id')} deleted product {product_id}")
    return None


@router.post("/{product_id}/image", response_model=ImageUploadResponse)
async def upload_product_image(
    product_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    admin: dict = Depends(get_admin_user)
):
    """
    Upload product image to S3.
    Requires admin privileges.
    """
    # Check if product exists
    product = product_service.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="PRODUCT_NOT_FOUND"
        )
    
    # Validate file type
    if file.content_type not in settings.allowed_file_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="INVALID_FILE_TYPE"
        )
    
    # Read file content
    file_content = await file.read()
    
    # Validate file size
    if len(file_content) > settings.max_file_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="FILE_TOO_LARGE"
        )
    
    # Get file extension
    file_extension = file.content_type.split("/")[1]
    
    try:
        # Upload to S3
        image_url = s3_service.upload_file(file_content, product_id, file_extension)
        
        # Update product
        product_service.update_product_image(db, product_id, image_url)
        
        logger.info(f"Admin {admin.get('user_id')} uploaded image for product {product_id}")
        return ImageUploadResponse(image_url=image_url)
        
    except Exception as e:
        logger.error(f"Error uploading image: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload image"
        )
