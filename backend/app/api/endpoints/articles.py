from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from bs4 import BeautifulSoup
from datetime import datetime

# 1. DB 및 모델 임포트 (절대 경로)
from app.database.connection import get_db
from app.models.article import Article

router = APIRouter()

# 2. Schema (여기서 직접 정의해서 유령 파일을 무시합니다)
class ArticleCreate(BaseModel):
    title: str
    content: str

# 3. 이미지 추출 함수
def get_first_image_src(html_content: str):
    if not html_content:
        return None
    try:
        soup = BeautifulSoup(html_content, "html.parser")
        img_tag = soup.find("img")
        return img_tag["src"] if img_tag and img_tag.get("src") else None
    except:
        return None

@router.get("/")
def read_articles(db: Session = Depends(get_db)):
    try:
        from app.services.news_service import fetch_and_store_google_news
        fetch_and_store_google_news(db)
    except Exception as e:
        print(f"뉴스 서비스 호출 실패: {e}")

    return db.query(Article).filter(Article.is_published == True)\
             .order_by(Article.published_at.desc()).all()

@router.post("/")
async def create_article(article_in: ArticleCreate, db: Session = Depends(get_db)):
    first_img = get_first_image_src(article_in.content)
    
    new_article = Article(
        title=article_in.title,
        content=article_in.content,
        thumbnail_url=first_img,
        author_id=1,
        is_published=True
    )
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article