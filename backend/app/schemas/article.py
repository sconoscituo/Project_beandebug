from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from ..models.article import ArticleCategory

class ArticleBase(BaseModel):
    title: str
    content: str
    category: ArticleCategory = ArticleCategory.GENERAL
    summary: Optional[str] = None
    thumbnail_url: Optional[str] = None
    is_published: bool = False

class ArticleCreate(ArticleBase):
    pass

class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[ArticleCategory] = None
    summary: Optional[str] = None
    thumbnail_url: Optional[str] = None
    is_published: Optional[bool] = None

class ArticleResponse(ArticleBase):
    id: int
    slug: str
    author_id: int
    view_count: int
    likes_count: int
    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True