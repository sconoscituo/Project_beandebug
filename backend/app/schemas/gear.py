from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from ..models.gear import GearType

class GearBase(BaseModel):
    name: str
    brand: Optional[str] = None
    model: Optional[str] = None
    gear_type: GearType
    description: Optional[str] = None
    image_url: Optional[str] = None
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    currency: str = "USD"
    specifications: Optional[str] = None
    is_recommended: bool = False
    recommendation_reason: Optional[str] = None

class GearCreate(GearBase):
    pass

class GearUpdate(BaseModel):
    name: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    gear_type: Optional[GearType] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    currency: Optional[str] = None
    specifications: Optional[str] = None
    is_recommended: Optional[bool] = None
    recommendation_reason: Optional[str] = None

class GearResponse(GearBase):
    id: int
    average_rating: float
    review_count: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True