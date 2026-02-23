import re
from datetime import datetime, timezone

def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    text = text.strip('-')
    timestamp = datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')
    return f"{text}-{timestamp}"
