from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from ..database.connection import get_db
from ..models import User
from ..schemas import (
    ArticleCreate, ArticleUpdate, ArticleResponse,
    ArticleCommentCreate, ArticleCommentResponse
)
from ..schemas.pagination import PaginatedResponse
from ..services import ArticleService
from ..utils.auth import get_current_active_user

router = APIRouter(prefix="/articles", tags=["Articles"])


@router.post("/", response_model=ArticleResponse, status_code=status.HTTP_201_CREATED)
def create_article(
    article: ArticleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    svc = ArticleService(db)
    return svc.create_article(article.model_dump(), current_user.id)


@router.get("/")
def get_articles(
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=100),
    published_only: bool = True,
    db: Session = Depends(get_db)
):
    svc = ArticleService(db)
    items, total = svc.get_articles(page, page_size, published_only)
    return PaginatedResponse.create(items, total, page, page_size)


@router.get("/my")
def get_my_articles(
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    svc = ArticleService(db)
    items, total = svc.get_my_articles(current_user.id, page, page_size)
    return PaginatedResponse.create(items, total, page, page_size)


@router.get("/{article_id}", response_model=ArticleResponse)
def get_article(article_id: int, db: Session = Depends(get_db)):
    svc = ArticleService(db)
    article = svc.get_article(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


@router.put("/{article_id}", response_model=ArticleResponse)
def update_article(
    article_id: int,
    article_update: ArticleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    svc = ArticleService(db)
    article = svc.update_article(article_id, current_user.id, article_update.model_dump(exclude_unset=True))
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    svc = ArticleService(db)
    if not svc.delete_article(article_id, current_user.id):
        raise HTTPException(status_code=404, detail="Article not found")
    return None


@router.post("/{article_id}/like", status_code=status.HTTP_201_CREATED)
def like_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    svc = ArticleService(db)
    error = svc.like_article(article_id, current_user.id)
    if error == "not_found":
        raise HTTPException(status_code=404, detail="Article not found")
    if error == "already_liked":
        raise HTTPException(status_code=400, detail="Already liked")
    return {"message": "Article liked"}


@router.delete("/{article_id}/like", status_code=status.HTTP_204_NO_CONTENT)
def unlike_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    svc = ArticleService(db)
    if not svc.unlike_article(article_id, current_user.id):
        raise HTTPException(status_code=404, detail="Like not found")
    return None


@router.post("/{article_id}/comments", response_model=ArticleCommentResponse, status_code=status.HTTP_201_CREATED)
def create_article_comment(
    article_id: int,
    comment: ArticleCommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    svc = ArticleService(db)
    result = svc.create_comment(article_id, current_user.id, comment.content, comment.parent_id)
    if not result:
        raise HTTPException(status_code=404, detail="Article not found")
    return result


@router.get("/{article_id}/comments", response_model=List[ArticleCommentResponse])
def get_article_comments(article_id: int, db: Session = Depends(get_db)):
    svc = ArticleService(db)
    return svc.get_comments(article_id)
