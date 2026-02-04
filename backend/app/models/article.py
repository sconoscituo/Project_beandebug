from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum
from ..database.connection import Base

class ArticleCategory(str, Enum):
    NEW_TECH = "new_tech"
    BREWING_GUIDE = "brewing_guide"
    BEAN_REVIEW = "bean_review"
    GEAR_REVIEW = "gear_review"
    COFFEE_CULTURE = "coffee_culture"
    GENERAL = "general"

class Article(Base):
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    slug = Column(String, unique=True, index=True)
    content = Column(Text, nullable=False)
    category = Column(SQLEnum(ArticleCategory), default=ArticleCategory.GENERAL)
    summary = Column(String)  # 요약
    thumbnail_url = Column(String)
    
    author_id = Column(Integer, ForeignKey("users.id"))
    is_published = Column(Boolean, default=False)
    
    # 통계
    view_count = Column(Integer, default=0)
    likes_count = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = Column(DateTime)
    
    # 관계
    author = relationship("User", back_populates="articles")
    comments = relationship("ArticleComment", back_populates="article", cascade="all, delete-orphan")
    likes = relationship("ArticleLike", back_populates="article", cascade="all, delete-orphan")