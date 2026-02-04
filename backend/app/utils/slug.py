import re
from datetime import datetime

def slugify(text: str) -> str:
    """문자열을 URL-safe slug로 변환"""
    # 소문자로 변환
    text = text.lower()
    # 특수문자를 하이픈으로 변환
    text = re.sub(r'[^\w\s-]', '', text)
    # 공백을 하이픈으로 변환
    text = re.sub(r'[-\s]+', '-', text)
    # 앞뒤 하이픈 제거
    text = text.strip('-')
    # 타임스탬프 추가로 고유성 보장
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    return f"{text}-{timestamp}"