from sqlalchemy import Column, Integer, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database.connection import Base

class RecipeComment(Base):
    __tablename__ = "recipe_comments"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    parent_id = Column(Integer, ForeignKey("recipe_comments.id"), nullable=True)  # 대댓글
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 관계
    recipe = relationship("Recipe", back_populates="comments")
    user = relationship("User", back_populates="recipe_comments")
    parent = relationship("RecipeComment", remote_side=[id], backref="replies")

class ArticleComment(Base):
    __tablename__ = "article_comments"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    article_id = Column(Integer, ForeignKey("articles.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    parent_id = Column(Integer, ForeignKey("article_comments.id"), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 관계
    article = relationship("Article", back_populates="comments")
    user = relationship("User", back_populates="article_comments")
    parent = relationship("ArticleComment", remote_side=[id], backref="replies")