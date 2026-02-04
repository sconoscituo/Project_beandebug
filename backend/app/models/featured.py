from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.connection import Base

class BeanOfTheMonth(Base):
    """이달의 원두"""
    __tablename__ = "bean_of_the_month"
    
    id = Column(Integer, primary_key=True, index=True)
    bean_id = Column(Integer, ForeignKey("beans.id"))
    month = Column(String, nullable=False, unique=True)  # "2026-02"
    title = Column(String)
    description = Column(Text)
    highlight = Column(Text)  # 특별한 점
    image_url = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 관계
    bean = relationship("Bean", back_populates="bean_of_month")

class FeaturedRecipe(Base):
    """피처드 레시피"""
    __tablename__ = "featured_recipes"
    
    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    category = Column(String)  # "variant_coffee", "classic", "experimental", "beginner_friendly"
    title = Column(String)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    display_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)  # 피처 만료일
    
    # 관계
    recipe = relationship("Recipe", back_populates="featured")