from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database.connection import Base

class Recipe(Base):
    __tablename__ = "recipes"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(Text)
    bean_id = Column(Integer, ForeignKey("beans.id"))
    
    # 추출 정보
    brew_method = Column(String)  # V60, Chemex, French Press, Espresso, Aeropress 등
    grind_size = Column(String)  # Fine, Medium-fine, Medium, Medium-coarse, Coarse
    water_temp = Column(Float)  # 섭씨 온도
    coffee_amount = Column(Float)  # 그램
    water_amount = Column(Float)  # ml
    brew_time = Column(Integer)  # 초
    ratio = Column(String)  # 비율 (e.g., "1:16")
    
    # 상세 레시피
    steps = Column(Text)  # 단계별 설명
    tips = Column(Text)  # 팁
    
    # 평가
    taste_rating = Column(Integer)  # 1-5
    body_rating = Column(Integer)  # 1-5
    acidity_rating = Column(Integer)  # 1-5
    sweetness_rating = Column(Integer)  # 1-5
    overall_rating = Column(Float)  # 전체 평점
    notes = Column(Text)  # 추출 노트
    
    # 커뮤니티 기능
    is_public = Column(Boolean, default=False)
    view_count = Column(Integer, default=0)
    likes_count = Column(Integer, default=0)
    
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 관계
    owner = relationship("User", back_populates="recipes")
    bean = relationship("Bean", back_populates="recipes")
    comments = relationship("RecipeComment", back_populates="recipe", cascade="all, delete-orphan")
    likes = relationship("RecipeLike", back_populates="recipe", cascade="all, delete-orphan")
    featured = relationship("FeaturedRecipe", back_populates="recipe")