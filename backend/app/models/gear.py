from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum
from app.database.connection import Base

class GearType(str, Enum):
    GRINDER = "grinder"
    BREWER = "brewer"
    ESPRESSO_MACHINE = "espresso_machine"
    KETTLE = "kettle"
    SCALE = "scale"
    FILTER = "filter"
    ACCESSORIES = "accessories"

class Gear(Base):
    __tablename__ = "gears"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    brand = Column(String)
    model = Column(String)
    gear_type = Column(SQLEnum(GearType), nullable=False)
    description = Column(Text)
    image_url = Column(String)
    
    # 가격 정보
    price_min = Column(Float)
    price_max = Column(Float)
    currency = Column(String, default="USD")
    
    # 스펙
    specifications = Column(Text)  # JSON 형태로 저장 가능
    
    # 추천 정보
    is_recommended = Column(Boolean, default=False)
    recommendation_reason = Column(Text)
    
    # 평점
    average_rating = Column(Float, default=0.0)
    review_count = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 관계
    reviews = relationship("GearReview", back_populates="gear", cascade="all, delete-orphan")