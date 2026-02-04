from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database.connection import Base

class Bean(Base):
    __tablename__ = "beans"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    origin = Column(String)  # 원산지
    farm = Column(String)  # 농장
    variety = Column(String)  # 품종 (e.g., Arabica, Robusta)
    roast_level = Column(String)  # Light, Medium, Dark
    processing = Column(String)  # Washed, Natural, Honey
    altitude = Column(String)  # 재배 고도
    flavor_notes = Column(Text)  # 풍미 노트
    tasting_notes = Column(Text)  # 시음 노트
    
    # 구매 정보
    purchase_date = Column(DateTime)
    roast_date = Column(DateTime)
    price = Column(Float)
    vendor = Column(String)  # 구매처
    
    # 공개 설정
    is_public = Column(Boolean, default=False)
    
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 관계
    owner = relationship("User", back_populates="beans")
    recipes = relationship("Recipe", back_populates="bean")
    bean_of_month = relationship("BeanOfTheMonth", back_populates="bean")