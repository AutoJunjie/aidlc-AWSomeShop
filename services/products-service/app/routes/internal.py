"""Internal API routes for service-to-service communication."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import ProductResponse
from app.services.product_service import product_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/internal/products", tags=["internal"])


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product_internal(
    product_id: int,
    db: Session = Depends(get_db)
):
    """
    Get product by ID (internal API - no authentication required).
    Used for service-to-service communication.
    """
    product = product_service.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="PRODUCT_NOT_FOUND"
        )
    return ProductResponse.model_validate(product)
