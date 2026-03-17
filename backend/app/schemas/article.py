from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ArticleBase(BaseModel):
    title: str
    content: str
    summary: Optional[str] = None
    thumbnail_url: Optional[str] = None
    is_published: bool = True

class ArticleCreate(ArticleBase):
    pass

class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    thumbnail_url: Optional[str] = None
    is_published: Optional[bool] = None

class ArticleResponse(ArticleBase):
    id: int
    author_id: Optional[int] = None
    view_count: int = 0
    likes_count: int = 0
    created_at: datetime
    published_at: Optional[datetime] = None

    class Config:
        from_attributes = True
