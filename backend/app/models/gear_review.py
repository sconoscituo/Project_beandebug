from sqlalchemy import Column, Integer, ForeignKey, DateTime, Text, Float, String
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database.connection import Base

class GearReview(Base):
    __tablename__ = "gear_reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    gear_id = Column(Integer, ForeignKey("gears.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    
    rating = Column(Float, nullable=False)  # 1-5
    title = Column(String)
    content = Column(Text)
    pros = Column(Text)  # 장점
    cons = Column(Text)  # 단점
    
    # 사용 기간
    usage_duration = Column(String)  # "6 months", "1 year" 등
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 관계
    gear = relationship("Gear", back_populates="reviews")
    user = relationship("User", back_populates="gear_reviews")