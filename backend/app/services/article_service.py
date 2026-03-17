from typing import Tuple, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from bs4 import BeautifulSoup

from ..models import Article, ArticleComment, ArticleLike
from ..repositories.base import BaseRepository
from ..core.logging import get_logger

logger = get_logger("service.article")


def extract_thumbnail(html_content: str) -> Optional[str]:
    if not html_content:
        return None
    try:
        soup = BeautifulSoup(html_content, "html.parser")
        img_tag = soup.find("img")
        if img_tag and img_tag.get("src"):
            return img_tag["src"]
    except Exception:
        pass
    return None


class ArticleService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = BaseRepository(Article, db)

    def create_article(self, article_data: dict, author_id: int) -> Article:
        thumbnail = extract_thumbnail(article_data.get("content", ""))
        article = Article(**article_data, author_id=author_id, thumbnail_url=thumbnail)
        logger.info(f"Creating article: {article_data.get('title')} by user {author_id}")
        return self.repo.create(article)

    def get_articles(
        self,
        page: int = 1,
        page_size: int = 12,
        published_only: bool = True,
    ) -> Tuple[List[Article], int]:
        filters = []
        if published_only:
            filters.append(Article.is_published == True)
        return self.repo.get_paginated(page, page_size, filters, desc(Article.created_at))

    def get_my_articles(
        self, author_id: int, page: int = 1, page_size: int = 12
    ) -> Tuple[List[Article], int]:
        filters = [Article.author_id == author_id]
        return self.repo.get_paginated(page, page_size, filters, desc(Article.created_at))

    def get_article(self, article_id: int) -> Optional[Article]:
        article = self.repo.get_by_id(article_id)
        if article:
            article.view_count += 1
            self.db.commit()
        return article

    def update_article(self, article_id: int, author_id: int, update_data: dict) -> Optional[Article]:
        article = (
            self.db.query(Article)
            .filter(Article.id == article_id, Article.author_id == author_id)
            .first()
        )
        if not article:
            return None
        return self.repo.update(article, update_data)

    def delete_article(self, article_id: int, author_id: int) -> bool:
        article = (
            self.db.query(Article)
            .filter(Article.id == article_id, Article.author_id == author_id)
            .first()
        )
        if not article:
            return False
        self.repo.delete(article)
        return True

    def like_article(self, article_id: int, user_id: int) -> Optional[str]:
        article = self.repo.get_by_id(article_id)
        if not article:
            return "not_found"
        existing = (
            self.db.query(ArticleLike)
            .filter(ArticleLike.article_id == article_id, ArticleLike.user_id == user_id)
            .first()
        )
        if existing:
            return "already_liked"
        self.db.add(ArticleLike(article_id=article_id, user_id=user_id))
        article.likes_count += 1
        self.db.commit()
        return None

    def unlike_article(self, article_id: int, user_id: int) -> bool:
        like = (
            self.db.query(ArticleLike)
            .filter(ArticleLike.article_id == article_id, ArticleLike.user_id == user_id)
            .first()
        )
        if not like:
            return False
        self.db.delete(like)
        article = self.repo.get_by_id(article_id)
        if article:
            article.likes_count = max(0, article.likes_count - 1)
        self.db.commit()
        return True

    def create_comment(self, article_id: int, user_id: int, content: str, parent_id: Optional[int] = None) -> Optional[ArticleComment]:
        article = self.repo.get_by_id(article_id)
        if not article:
            return None
        comment = ArticleComment(
            content=content, article_id=article_id, user_id=user_id, parent_id=parent_id
        )
        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)
        return comment

    def get_comments(self, article_id: int) -> List[ArticleComment]:
        return (
            self.db.query(ArticleComment)
            .filter(ArticleComment.article_id == article_id)
            .order_by(ArticleComment.created_at)
            .all()
        )
