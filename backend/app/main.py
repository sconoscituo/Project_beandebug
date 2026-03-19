from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import os

from .database.connection import engine, Base, settings, get_db
from .routers import (
    auth_router, beans_router, recipes_router,
    articles_router, gears_router, featured_router,
    subscriptions_router, ai_debug_router
)
from .core.config import get_global_config
from .core.logging import setup_logging, get_logger
from .core.security import SecurityMiddleware
from .services import SeedFactory

config = get_global_config()
setup_logging(settings.debug)
logger = get_logger("main")

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=config.APP_NAME,
    description="Coffee brewing recipe management and community platform - Debug your coffee!",
    version=config.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)
app.mount("/media", StaticFiles(directory="uploads"), name="media")

allowed_origins = [o.strip() for o in settings.allowed_origins.split(",") if o.strip()]

app.add_middleware(SecurityMiddleware)
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
app.include_router(subscriptions_router)
app.include_router(ai_debug_router)


@app.get("/")
def read_root():
    return {
        "message": f"Welcome to {config.APP_NAME} API",
        "tagline": "Debug your coffee, one brew at a time",
        "version": config.APP_VERSION,
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": config.APP_NAME}


@app.post("/seed")
def seed_database(db: Session = Depends(get_db)):
    factory = SeedFactory(db)
    result = factory.seed_all()
    logger.info(f"Seed result: {result}")
    return result
