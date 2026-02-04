from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from ..database.connection import get_db
from ..models import Article, User, ArticleComment, ArticleLike
from ..models.article import ArticleCategory
from ..schemas import (
    ArticleCreate,
    ArticleUpdate,
    ArticleResponse,
    ArticleCommentCreate,
    ArticleCommentResponse
)
from ..utils.auth import get_current_active_user, get_current_admin_user
from ..utils.slug import slugify

router = APIRouter(prefix="/articles", tags=["Articles"])

@router.post("/", response_model=ArticleResponse, status_code=status.HTTP_201_CREATED)
def create_article(
    article: ArticleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """아티클 생성"""
    slug = slugify(article.title)
    
    db_article = Article(
        **article.dict(),
        slug=slug,
        author_id=current_user.id
    )
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    
    return db_article

@router.get("/", response_model=List[ArticleResponse])
def get_articles(
    skip: int = 0,
    limit: int = 100,
    category: ArticleCategory = Query(None),
    published_only: bool = True,
    db: Session = Depends(get_db)
):
    """아티클 목록"""
    query = db.query(Article)
    
    if published_only:
        query = query.filter(Article.is_published == True)
    
    if category:
        query = query.filter(Article.category == category)
    
    articles = query.order_by(desc(Article.created_at)).offset(skip).limit(limit).all()
    return articles

@router.get("/my", response_model=List[ArticleResponse])
def get_my_articles(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """내 아티클 목록"""
    articles = db.query(Article).filter(
        Article.author_id == current_user.id
    ).order_by(desc(Article.created_at)).offset(skip).limit(limit).all()
    
    return articles

@router.get("/{article_id}", response_model=ArticleResponse)
def get_article(
    article_id: int,
    db: Session = Depends(get_db)
):
    """아티클 상세"""
    article = db.query(Article).filter(
        Article.id == article_id,
        Article.is_published == True
    ).first()
    
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    # 조회수 증가
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
    """아티클 수정"""
    article = db.query(Article).filter(
        Article.id == article_id,
        Article.author_id == current_user.id
    ).first()
    
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    update_data = article_update.dict(exclude_unset=True)
    
    # 제목이 변경되면 slug도 업데이트
    if "title" in update_data:
        update_data["slug"] = slugify(update_data["title"])
    
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
    """아티클 삭제"""
    article = db.query(Article).filter(
        Article.id == article_id,
        Article.author_id == current_user.id
    ).first()
    
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    db.delete(article)
    db.commit()
    return None

# 좋아요
@router.post("/{article_id}/like", status_code=status.HTTP_201_CREATED)
def like_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """아티클 좋아요"""
    article = db.query(Article).filter(
        Article.id == article_id,
        Article.is_published == True
    ).first()
    
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    existing_like = db.query(ArticleLike).filter(
        ArticleLike.article_id == article_id,
        ArticleLike.user_id == current_user.id
    ).first()
    
    if existing_like:
        raise HTTPException(status_code=400, detail="Already liked")
    
    like = ArticleLike(article_id=article_id, user_id=current_user.id)
    db.add(like)
    
    article.likes_count += 1
    db.commit()
    
    return {"message": "Article liked"}

@router.delete("/{article_id}/like", status_code=status.HTTP_204_NO_CONTENT)
def unlike_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """아티클 좋아요 취소"""
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

# 댓글
@router.post("/{article_id}/comments", response_model=ArticleCommentResponse, status_code=status.HTTP_201_CREATED)
def create_article_comment(
    article_id: int,
    comment: ArticleCommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """아티클 댓글 작성"""
    article = db.query(Article).filter(
        Article.id == article_id,
        Article.is_published == True
    ).first()
    
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
    """아티클 댓글 목록"""
    comments = db.query(ArticleComment).filter(
        ArticleComment.article_id == article_id
    ).order_by(ArticleComment.created_at).all()
    
    return comments