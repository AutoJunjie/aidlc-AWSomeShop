"""Pydantic schemas for request/response validation."""
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime


class ProductBase(BaseModel):
    """Base product schema."""
    name: str = Field(..., min_length=1, max_length=100, description="Product name")
    description: Optional[str] = Field(None, max_length=1000, description="Product description")
    points_cost: int = Field(..., gt=0, description="Points cost (must be positive)")


class ProductCreate(ProductBase):
    """Schema for creating a product."""
    image_url: Optional[str] = Field(None, max_length=500)


class ProductUpdate(BaseModel):
    """Schema for updating a product."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    points_cost: Optional[int] = Field(None, gt=0)
    image_url: Optional[str] = Field(None, max_length=500)
    is_active: Optional[bool] = None


class ProductResponse(ProductBase):
    """Schema for product response."""
    id: int
    image_url: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    """Schema for product list response."""
    products: list[ProductResponse]


class ImageUploadResponse(BaseModel):
    """Schema for image upload response."""
    image_url: str


class ErrorResponse(BaseModel):
    """Schema for error response."""
    error: str
    detail: Optional[str] = None


class HealthCheckResponse(BaseModel):
    """Schema for health check response."""
    status: str
    database: bool
    s3: bool
