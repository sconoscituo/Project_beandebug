from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from ..database.connection import get_db
from ..models import User
from ..models.subscription import SubscriptionPlan, UserSubscription, PlanType
from ..utils.auth import get_current_active_user

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_user_plan(user: User, db: Session) -> SubscriptionPlan | None:
    if user.subscription and user.subscription.is_active:
        return user.subscription.plan
    return None


def _require_premium(user: User, db: Session) -> None:
    plan = _get_user_plan(user, db)
    if plan is None or plan.plan_type != PlanType.premium:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Premium subscription required",
        )


# ---------------------------------------------------------------------------
# Public endpoints
# ---------------------------------------------------------------------------

@router.get("/plans")
def list_plans(db: Session = Depends(get_db)):
    """모든 구독 플랜 목록을 반환합니다."""
    plans = db.query(SubscriptionPlan).all()
    return [
        {
            "id": p.id,
            "name": p.name,
            "plan_type": p.plan_type,
            "price_monthly": p.price_monthly,
            "ai_debug_enabled": p.ai_debug_enabled,
            "code_review_enabled": p.code_review_enabled,
            "max_posts_per_day": p.max_posts_per_day,
            "description": p.description,
        }
        for p in plans
    ]


@router.get("/me")
def my_subscription(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """현재 로그인한 사용자의 구독 정보를 반환합니다."""
    sub = current_user.subscription
    if sub is None:
        return {"plan_type": PlanType.free, "is_active": False, "expires_at": None}
    return {
        "plan_type": sub.plan.plan_type if sub.plan else PlanType.free,
        "plan_name": sub.plan.name if sub.plan else "Free",
        "is_active": sub.is_active,
        "started_at": sub.started_at,
        "expires_at": sub.expires_at,
        "ai_debug_enabled": sub.plan.ai_debug_enabled if sub.plan else False,
        "code_review_enabled": sub.plan.code_review_enabled if sub.plan else False,
    }


@router.post("/upgrade")
def upgrade_to_premium(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """무료 사용자를 프리미엄으로 업그레이드합니다. (결제 연동 전 skeleton)"""
    premium_plan = (
        db.query(SubscriptionPlan)
        .filter(SubscriptionPlan.plan_type == PlanType.premium)
        .first()
    )
    if premium_plan is None:
        raise HTTPException(status_code=404, detail="Premium plan not configured")

    sub = current_user.subscription
    if sub is not None:
        if sub.plan.plan_type == PlanType.premium and sub.is_active:
            raise HTTPException(status_code=400, detail="Already on premium plan")
        sub.plan_id = premium_plan.id
        sub.is_active = True
        sub.started_at = datetime.now(timezone.utc)
        sub.expires_at = None
    else:
        sub = UserSubscription(
            user_id=current_user.id,
            plan_id=premium_plan.id,
            is_active=True,
        )
        db.add(sub)

    db.commit()
    db.refresh(sub)
    return {"message": "Upgraded to premium", "plan_type": PlanType.premium}


@router.post("/downgrade")
def downgrade_to_free(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """프리미엄 구독을 무료로 다운그레이드합니다."""
    free_plan = (
        db.query(SubscriptionPlan)
        .filter(SubscriptionPlan.plan_type == PlanType.free)
        .first()
    )
    if free_plan is None:
        raise HTTPException(status_code=404, detail="Free plan not configured")

    sub = current_user.subscription
    if sub is None or sub.plan.plan_type == PlanType.free:
        raise HTTPException(status_code=400, detail="Already on free plan")

    sub.plan_id = free_plan.id
    sub.is_active = True
    sub.expires_at = None
    db.commit()
    return {"message": "Downgraded to free plan"}


# ---------------------------------------------------------------------------
# Premium-only: AI Debugging (skeleton)
# ---------------------------------------------------------------------------

@router.post("/ai-debug")
def ai_debug(
    payload: dict,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """[Premium] 코드 스니펫을 받아 AI 디버깅 결과를 반환합니다.

    현재는 skeleton으로 실제 LLM 연동은 추후 구현합니다.
    """
    _require_premium(current_user, db)

    code = payload.get("code", "")
    language = payload.get("language", "python")

    if not code:
        raise HTTPException(status_code=422, detail="code field is required")

    # TODO: LLM API 연동 (OpenAI / Anthropic)
    return {
        "status": "ok",
        "language": language,
        "analysis": "AI 디버깅 분석 결과가 여기에 표시됩니다. (LLM 연동 예정)",
        "suggestions": [
            "코드 스타일을 확인하세요.",
            "예외 처리를 추가하는 것을 권장합니다.",
        ],
    }


@router.post("/code-review")
def code_review(
    payload: dict,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """[Premium] 코드 리뷰를 요청합니다. (skeleton)"""
    _require_premium(current_user, db)

    code = payload.get("code", "")
    if not code:
        raise HTTPException(status_code=422, detail="code field is required")

    # TODO: LLM API 연동
    return {
        "status": "ok",
        "review": "코드 리뷰 결과가 여기에 표시됩니다. (LLM 연동 예정)",
        "score": None,
    }
