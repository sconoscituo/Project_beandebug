import time
import hashlib
from collections import defaultdict
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from .config import get_global_config
from .logging import get_logger

logger = get_logger("security")
config = get_global_config()


class RateLimitStore:
    def __init__(self):
        self._requests = defaultdict(list)

    def is_rate_limited(self, client_ip: str) -> bool:
        now = time.time()
        window = config.RATE_LIMIT_WINDOW_SECONDS
        self._requests[client_ip] = [
            ts for ts in self._requests[client_ip] if now - ts < window
        ]
        if len(self._requests[client_ip]) >= config.RATE_LIMIT_REQUESTS:
            return True
        self._requests[client_ip].append(now)
        return False


_rate_limiter = RateLimitStore()


class SecurityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        client_ip = request.client.host if request.client else "unknown"

        if _rate_limiter.is_rate_limited(client_ip):
            logger.warning(f"Rate limited: {client_ip}")
            return JSONResponse(
                status_code=429,
                content={"detail": "Too many requests. Please try again later."},
            )

        request_id = hashlib.md5(
            f"{client_ip}{time.time()}".encode()
        ).hexdigest()[:12]

        response = await call_next(request)

        duration_ms = round((time.time() - start_time) * 1000, 2)

        response.headers["X-Request-ID"] = request_id
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Cache-Control"] = "no-store"

        logger.info(
            f"{request.method} {request.url.path} {response.status_code} {duration_ms}ms"
        )

        return response
