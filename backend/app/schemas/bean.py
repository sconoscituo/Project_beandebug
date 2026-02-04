from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class BeanBase(BaseModel):
    name: str
    origin: Optional[str] = None
    farm: Optional[str] = None
    variety: Optional[str] = None
    roast_level: Optional[str] = None
    processing: Optional[str] = None
    altitude: Optional[str] = None
    flavor_notes: Optional[str] = None
    tasting_notes: Optional[str] = None
    purchase_date: Optional[datetime] = None
    roast_date: Optional[datetime] = None
    price: Optional[float] = None
    vendor: Optional[str] = None
    is_public: bool = False

class BeanCreate(BeanBase):
    pass

class BeanUpdate(BaseModel):
    name: Optional[str] = None
    origin: Optional[str] = None
    farm: Optional[str] = None
    variety: Optional[str] = None
    roast_level: Optional[str] = None
    processing: Optional[str] = None
    altitude: Optional[str] = None
    flavor_notes: Optional[str] = None
    tasting_notes: Optional[str] = None
    purchase_date: Optional[datetime] = None
    roast_date: Optional[datetime] = None
    price: Optional[float] = None
    vendor: Optional[str] = None
    is_public: Optional[bool] = None

class BeanResponse(BeanBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True