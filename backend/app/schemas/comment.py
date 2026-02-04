from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CommentBase(BaseModel):
    content: str
    parent_id: Optional[int] = None

class RecipeCommentCreate(CommentBase):
    recipe_id: int

class ArticleCommentCreate(CommentBase):
    article_id: int

class CommentUpdate(BaseModel):
    content: str

class RecipeCommentResponse(CommentBase):
    id: int
    recipe_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ArticleCommentResponse(CommentBase):
    id: int
    article_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True