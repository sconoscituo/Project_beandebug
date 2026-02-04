from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class GearReviewBase(BaseModel):
    gear_id: int
    rating: float = Field(..., ge=1, le=5)
    title: Optional[str] = None
    content: Optional[str] = None
    pros: Optional[str] = None
    cons: Optional[str] = None
    usage_duration: Optional[str] = None

class GearReviewCreate(GearReviewBase):
    pass

class GearReviewUpdate(BaseModel):
    rating: Optional[float] = Field(None, ge=1, le=5)
    title: Optional[str] = None
    content: Optional[str] = None
    pros: Optional[str] = None
    cons: Optional[str] = None
    usage_duration: Optional[str] = None

class GearReviewResponse(GearReviewBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True