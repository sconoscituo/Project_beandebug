from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RecipeBase(BaseModel):
    title: str
    description: Optional[str] = None
    bean_id: int
    brew_method: Optional[str] = None
    grind_size: Optional[str] = None
    water_temp: Optional[float] = None
    coffee_amount: Optional[float] = None
    water_amount: Optional[float] = None
    brew_time: Optional[int] = None
    ratio: Optional[str] = None
    steps: Optional[str] = None
    tips: Optional[str] = None
    taste_rating: Optional[int] = None
    body_rating: Optional[int] = None
    acidity_rating: Optional[int] = None
    sweetness_rating: Optional[int] = None
    overall_rating: Optional[float] = None
    notes: Optional[str] = None
    is_public: bool = False

class RecipeCreate(RecipeBase):
    pass

class RecipeUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    bean_id: Optional[int] = None
    brew_method: Optional[str] = None
    grind_size: Optional[str] = None
    water_temp: Optional[float] = None
    coffee_amount: Optional[float] = None
    water_amount: Optional[float] = None
    brew_time: Optional[int] = None
    ratio: Optional[str] = None
    steps: Optional[str] = None
    tips: Optional[str] = None
    taste_rating: Optional[int] = None
    body_rating: Optional[int] = None
    acidity_rating: Optional[int] = None
    sweetness_rating: Optional[int] = None
    overall_rating: Optional[float] = None
    notes: Optional[str] = None
    is_public: Optional[bool] = None

class RecipeResponse(RecipeBase):
    id: int
    owner_id: int
    view_count: int
    likes_count: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True