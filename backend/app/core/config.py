from functools import lru_cache


class GlobalConfig:
    APP_NAME = "Bean Debug"
    APP_VERSION = "1.0.0"
    API_PREFIX = ""

    # Pagination
    DEFAULT_PAGE = 1
    DEFAULT_PAGE_SIZE = 12
    MAX_PAGE_SIZE = 100

    # Rate Limiting
    RATE_LIMIT_REQUESTS = 100
    RATE_LIMIT_WINDOW_SECONDS = 60

    # Security
    CORS_MAX_AGE = 600
    TOKEN_ALGORITHM = "HS256"
    PASSWORD_MIN_LENGTH = 8
    PASSWORD_MAX_LENGTH = 72

    # Content
    MAX_TITLE_LENGTH = 200
    MAX_CONTENT_LENGTH = 50000
    MAX_COMMENT_LENGTH = 2000
    ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}

    # Cost Optimization
    QUERY_BATCH_SIZE = 50
    CACHE_TTL_SECONDS = 300
    DB_POOL_SIZE = 5
    DB_MAX_OVERFLOW = 10
    DB_POOL_RECYCLE = 3600

    # Seed Data
    SEED_USERS_COUNT = 5
    SEED_BEANS_COUNT = 30
    SEED_RECIPES_COUNT = 40
    SEED_ARTICLES_COUNT = 25
    SEED_GEARS_COUNT = 20
    SEED_REVIEWS_PER_GEAR = 3


@lru_cache()
def get_global_config() -> GlobalConfig:
    return GlobalConfig()
