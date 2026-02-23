# backend/app/services/news_service.py
from GoogleNews import GoogleNews # pip install GoogleNews
import datetime

def get_coffee_news_from_google(keyword="스페셜티 커피"):
    googlenews = GoogleNews(lang='ko', region='KR', period='7d')
    googlenews.search(keyword)
    results = googlenews.results()
    formatted_articles = []
    for i, item in enumerate(results[:10]):
        formatted_articles.append({
            "id": i + 1,
            "title": item.get('title'),
            "category": "news",
            "summary": item.get('desc') or f"{keyword} 관련 최신 소식입니다.",
            "author": item.get('media'),
            "created_at": item.get('date') or datetime.date.today().isoformat(),
            "read_time": 5, 
            "likes": 0,
            "link": item.get('link')
        })
    
    return formatted_articles