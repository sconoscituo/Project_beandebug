from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class BeanOfTheMonthBase(BaseModel):
    bean_id: int
    month: str
    title: Optional[str] = None
    description: Optional[str] = None
    highlight: Optional[str] = None
    image_url: Optional[str] = None
    is_active: bool = True

class BeanOfTheMonthCreate(BeanOfTheMonthBase):
    pass

class BeanOfTheMonthResponse(BeanOfTheMonthBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class FeaturedRecipeBase(BaseModel):
    recipe_id: int
    category: str
    title: Optional[str] = None
    description: Optional[str] = None
    is_active: bool = True
    display_order: int = 0
    expires_at: Optional[datetime] = None

class FeaturedRecipeCreate(FeaturedRecipeBase):
    pass

class FeaturedRecipeResponse(FeaturedRecipeBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True