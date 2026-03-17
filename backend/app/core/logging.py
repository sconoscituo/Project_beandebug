import logging
import sys
from datetime import datetime, timezone


class StructuredFormatter(logging.Formatter):
    def format(self, record):
        timestamp = datetime.now(timezone.utc).isoformat()
        level = record.levelname
        module = record.module
        message = record.getMessage()
        extra = ""
        if hasattr(record, "request_id"):
            extra += f" request_id={record.request_id}"
        if hasattr(record, "user_id"):
            extra += f" user_id={record.user_id}"
        if hasattr(record, "duration_ms"):
            extra += f" duration_ms={record.duration_ms}"
        return f"[{timestamp}] {level} {module}: {message}{extra}"


def setup_logging(debug: bool = False) -> None:
    level = logging.DEBUG if debug else logging.INFO
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(StructuredFormatter())
    root_logger = logging.getLogger("beandebug")
    root_logger.setLevel(level)
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(f"beandebug.{name}")
