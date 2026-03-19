"""
AI 디버깅 API 라우터 (프리미엄 전용).
에러 분석 및 코드 리뷰 엔드포인트를 제공합니다.
"""

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from ..database.connection import get_db
from ..models import User
from ..models.subscription import PlanType
from ..services.ai_debugger import analyze_error, review_code
from ..utils.auth import get_current_active_user

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/ai", tags=["AI Debugging"])

SUPPORTED_LANGUAGES = {
    "python", "javascript", "typescript", "java", "kotlin",
    "swift", "go", "rust", "cpp", "c", "csharp", "php",
    "ruby", "dart", "sql", "bash", "other",
}


class DebugRequest(BaseModel):
    error_message: str = Field(..., min_length=1, max_length=5000, description="에러 메시지 또는 스택 트레이스")
    code_snippet: str = Field(default="", max_length=10000, description="에러가 발생한 코드 (선택사항)")
    language: str = Field(default="python", description="프로그래밍 언어")


class ReviewRequest(BaseModel):
    code: str = Field(..., min_length=1, max_length=10000, description="리뷰할 코드")
    language: str = Field(default="python", description="프로그래밍 언어")


def _require_premium(user: User, db: Session) -> None:
    """프리미엄 구독 여부를 확인합니다. 비프리미엄이면 403 예외를 발생시킵니다."""
    sub = user.subscription
    if sub is None or not sub.is_active or sub.plan is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="이 기능은 프리미엄 구독자 전용입니다.",
        )
    if sub.plan.plan_type != PlanType.premium:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="이 기능은 프리미엄 구독자 전용입니다.",
        )


@router.post("/debug")
async def debug_error(
    body: DebugRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    [프리미엄 전용] 에러 메시지와 코드를 분석하여 원인 및 해결책을 제시합니다.

    - error_message: 발생한 에러 메시지 또는 스택 트레이스 (필수)
    - code_snippet: 에러가 발생한 코드 (선택사항, 제공 시 더 정확한 분석)
    - language: 프로그래밍 언어 (기본값: python)
    """
    _require_premium(current_user, db)

    language = body.language.lower()
    if language not in SUPPORTED_LANGUAGES:
        language = "other"

    logger.info(
        "AI debug request: user=%s, language=%s, error_len=%d",
        current_user.id, language, len(body.error_message),
    )

    result = await analyze_error(
        error_message=body.error_message,
        code_snippet=body.code_snippet,
        language=language,
    )

    return {
        "success": True,
        "language": language,
        "data": result,
    }


@router.post("/review")
async def review_code_endpoint(
    body: ReviewRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    [프리미엄 전용] 코드를 리뷰하여 버그, 성능, 보안 이슈를 분석합니다.

    - code: 리뷰할 코드 (필수)
    - language: 프로그래밍 언어 (기본값: python)
    """
    _require_premium(current_user, db)

    language = body.language.lower()
    if language not in SUPPORTED_LANGUAGES:
        language = "other"

    logger.info(
        "AI review request: user=%s, language=%s, code_len=%d",
        current_user.id, language, len(body.code),
    )

    result = await review_code(
        code=body.code,
        language=language,
    )

    return {
        "success": True,
        "language": language,
        "data": result,
    }
