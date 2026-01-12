"""Database models for Products Service."""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Product(Base):
    """Product model."""
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(1000), nullable=True)
    points_cost = Column(Integer, nullable=False)
    image_url = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "points_cost": self.points_cost,
            "image_url": self.image_url,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
