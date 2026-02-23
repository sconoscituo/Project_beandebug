from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from ..database.connection import Base

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    thumbnail_url = Column(String(1000), nullable=True)
    author_id = Column(Integer, nullable=True)
    is_published = Column(Boolean, default=True)
    view_count = Column(Integer, default=0)
    likes_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    published_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    comments = relationship("ArticleComment", back_populates="article", cascade="all, delete-orphan")
    likes = relationship("ArticleLike", back_populates="article", cascade="all, delete-orphan")
