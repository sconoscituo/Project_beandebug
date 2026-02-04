from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database.connection import Base

class RecipeLike(Base):
    __tablename__ = "recipe_likes"
    __table_args__ = (UniqueConstraint('recipe_id', 'user_id', name='unique_recipe_like'),)
    
    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 관계
    recipe = relationship("Recipe", back_populates="likes")
    user = relationship("User", back_populates="recipe_likes")

class ArticleLike(Base):
    __tablename__ = "article_likes"
    __table_args__ = (UniqueConstraint('article_id', 'user_id', name='unique_article_like'),)
    
    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey("articles.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 관계
    article = relationship("Article", back_populates="likes")
    user = relationship("User", back_populates="article_likes")