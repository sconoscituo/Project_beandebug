from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from bs4 import BeautifulSoup

from ..database.connection import get_db
from ..models import Article, User, ArticleComment, ArticleLike
from ..schemas import (
    ArticleCreate,
    ArticleUpdate,
    ArticleResponse,
    ArticleCommentCreate,
    ArticleCommentResponse
)
from ..utils.auth import get_current_active_user
from ..utils.slug import slugify

router = APIRouter(prefix="/articles", tags=["Articles"])

def get_first_image_src(html_content: str):
    if not html_content:
        return None
    try:
        soup = BeautifulSoup(html_content, "html.parser")
        img_tag = soup.find("img")
        if img_tag and img_tag.get("src"):
            return img_tag["src"]
    except Exception:
        return None
    return None

@router.post("/", response_model=ArticleResponse, status_code=status.HTTP_201_CREATED)
def create_article(
    article: ArticleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    extracted_thumbnail = get_first_image_src(article.content)
    db_article = Article(
        **article.model_dump(),
        author_id=current_user.id,
        thumbnail_url=extracted_thumbnail
    )
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article

@router.get("/", response_model=List[ArticleResponse])
def get_articles(
    skip: int = 0,
    limit: int = 100,
    published_only: bool = True,
    db: Session = Depends(get_db)
):
    try:
        from ..services.news_service import fetch_and_store_google_news
        fetch_and_store_google_news(db)
    except Exception as e:
        print(f"뉴스 수집 실패: {e}")

    query = db.query(Article)
    if published_only:
        query = query.filter(Article.is_published == True)
    return query.order_by(desc(Article.created_at)).offset(skip).limit(limit).all()

@router.get("/my", response_model=List[ArticleResponse])
def get_my_articles(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return db.query(Article).filter(
        Article.author_id == current_user.id
    ).order_by(desc(Article.created_at)).offset(skip).limit(limit).all()

@router.get("/{article_id}", response_model=ArticleResponse)
def get_article(
    article_id: int,
    db: Session = Depends(get_db)
):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    article.view_count += 1
    db.commit()
    return article

@router.put("/{article_id}", response_model=ArticleResponse)
def update_article(
    article_id: int,
    article_update: ArticleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    article = db.query(Article).filter(
        Article.id == article_id,
        Article.author_id == current_user.id
    ).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    update_data = article_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(article, field, value)
    db.commit()
    db.refresh(article)
    return article

@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    article = db.query(Article).filter(
        Article.id == article_id,
        Article.author_id == current_user.id
    ).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    db.delete(article)
    db.commit()
    return None

@router.post("/{article_id}/like", status_code=status.HTTP_201_CREATED)
def like_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    existing = db.query(ArticleLike).filter(
        ArticleLike.article_id == article_id,
        ArticleLike.user_id == current_user.id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already liked")
    db.add(ArticleLike(article_id=article_id, user_id=current_user.id))
    article.likes_count += 1
    db.commit()
    return {"message": "Article liked"}

@router.delete("/{article_id}/like", status_code=status.HTTP_204_NO_CONTENT)
def unlike_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    like = db.query(ArticleLike).filter(
        ArticleLike.article_id == article_id,
        ArticleLike.user_id == current_user.id
    ).first()
    if not like:
        raise HTTPException(status_code=404, detail="Like not found")
    db.delete(like)
    article = db.query(Article).filter(Article.id == article_id).first()
    if article:
        article.likes_count = max(0, article.likes_count - 1)
    db.commit()
    return None

@router.post("/{article_id}/comments", response_model=ArticleCommentResponse, status_code=status.HTTP_201_CREATED)
def create_article_comment(
    article_id: int,
    comment: ArticleCommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    db_comment = ArticleComment(
        content=comment.content,
        article_id=article_id,
        user_id=current_user.id,
        parent_id=comment.parent_id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

@router.get("/{article_id}/comments", response_model=List[ArticleCommentResponse])
def get_article_comments(
    article_id: int,
    db: Session = Depends(get_db)
):
    return db.query(ArticleComment).filter(
        ArticleComment.article_id == article_id
    ).order_by(ArticleComment.created_at).all()
