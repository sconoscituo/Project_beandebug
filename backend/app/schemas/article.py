from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# ArticleCategory 임포트 줄을 완전히 삭제했습니다.

class ArticleBase(BaseModel):
    title: str
    content: str
    # category 필드를 삭제했습니다.
    summary: Optional[str] = None
    thumbnail_url: Optional[str] = None
    is_published: bool = True  # 기본값을 True로 변경 (뉴스 수집 시 바로 보이게)

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
    # slug가 모델에 없다면 에러가 날 수 있으니, 모델에 맞춰 필드를 조정하세요.
    author_id: Optional[int] = None
    view_count: int = 0
    created_at: datetime
    published_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True