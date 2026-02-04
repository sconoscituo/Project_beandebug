from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database.connection import engine, Base, settings
from .routers import (
    auth_router,
    beans_router,
    recipes_router,
    articles_router,
    gears_router,
    featured_router
)

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    description="Coffee brewing recipe management and community platform - Debug your coffee!",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인만 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(auth_router)
app.include_router(beans_router)
app.include_router(recipes_router)
app.include_router(articles_router)
app.include_router(gears_router)
app.include_router(featured_router)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to Bean Debug API",
        "tagline": "Debug your coffee, one brew at a time",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": settings.app_name
    }