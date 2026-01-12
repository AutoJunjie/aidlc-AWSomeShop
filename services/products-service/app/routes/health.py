"""Health check route."""
from fastapi import APIRouter
from app.schemas import HealthCheckResponse
from app.database import check_db_connection
from app.services.s3_service import s3_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """
    Health check endpoint.
    Checks database and S3 connections.
    """
    db_ok = check_db_connection()
    s3_ok = s3_service.check_connection()
    
    status = "healthy" if (db_ok and s3_ok) else "unhealthy"
    
    logger.info(f"Health check: status={status}, db={db_ok}, s3={s3_ok}")
    
    return HealthCheckResponse(
        status=status,
        database=db_ok,
        s3=s3_ok
    )
