from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from .database.connection import engine, Base, settings
from .routers import (
    auth_router,
    beans_router,
    recipes_router,
    articles_router,
    gears_router,
    featured_router
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    description="Coffee brewing recipe management and community platform - Debug your coffee!",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)
app.mount("/media", StaticFiles(directory="uploads"), name="media")

allowed_origins = [o.strip() for o in settings.allowed_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
