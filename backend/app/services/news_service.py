from GoogleNews import GoogleNews
from sqlalchemy.orm import Session
from ..models.article import Article
import re
from datetime import datetime, timezone
from bs4 import BeautifulSoup

def extract_first_image(html_content: str):
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

def fetch_and_store_google_news(db: Session):
    googlenews = GoogleNews(lang='ko', period='1d')
    googlenews.search('커피 기술')

    results = googlenews.results()
    count = 0

    for item in results:
        title = item.get('title')
        existing_article = db.query(Article).filter(Article.title == title).first()
        if existing_article:
            continue

        content_html = item.get('desc', '') or item.get('link', '')

        image_url = item.get('img')
        if not image_url:
            image_url = extract_first_image(content_html)

        new_article = Article(
            title=title,
            content=content_html,
            thumbnail_url=image_url,
            is_published=True,
            published_at=datetime.now(timezone.utc)
        )

        db.add(new_article)
        count += 1

    if count > 0:
        db.commit()

    return count
