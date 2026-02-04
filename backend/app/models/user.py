from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database.connection import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    bio = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 관계 설정
    recipes = relationship("Recipe", back_populates="owner", cascade="all, delete-orphan")
    beans = relationship("Bean", back_populates="owner", cascade="all, delete-orphan")
    articles = relationship("Article", back_populates="author", cascade="all, delete-orphan")
    gear_reviews = relationship("GearReview", back_populates="user", cascade="all, delete-orphan")
    recipe_comments = relationship("RecipeComment", back_populates="user", cascade="all, delete-orphan")
    article_comments = relationship("ArticleComment", back_populates="user", cascade="all, delete-orphan")
    recipe_likes = relationship("RecipeLike", back_populates="user", cascade="all, delete-orphan")
    article_likes = relationship("ArticleLike", back_populates="user", cascade="all, delete-orphan")