"""구독 플랜 엔드포인트 테스트"""

import pytest
from backend.app.models.subscription import SubscriptionPlan, PlanType


@pytest.fixture()
def seed_plans(db):
    free_plan = SubscriptionPlan(
        name="Free",
        plan_type=PlanType.free,
        price_monthly=0,
        ai_debug_enabled=False,
        code_review_enabled=False,
        max_posts_per_day=5,
        description="기본 커뮤니티 기능",
    )
    premium_plan = SubscriptionPlan(
        name="Premium",
        plan_type=PlanType.premium,
        price_monthly=9900,
        ai_debug_enabled=True,
        code_review_enabled=True,
        max_posts_per_day=-1,
        description="AI 디버깅 + 코드 리뷰 무제한",
    )
    db.add_all([free_plan, premium_plan])
    db.commit()
    return free_plan, premium_plan


@pytest.fixture()
def auth_headers(client):
    client.post(
        "/auth/register",
        json={
            "email": "sub_tester@beandebug.dev",
            "username": "sub_tester",
            "password": "securepass123",
            "full_name": "Sub Tester",
        },
    )
    login_res = client.post(
        "/auth/login",
        data={"username": "sub_tester", "password": "securepass123"},
    )
    token = login_res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_list_plans(client, seed_plans):
    res = client.get("/subscriptions/plans")
    assert res.status_code == 200
    plans = res.json()
    assert len(plans) >= 2
    plan_types = [p["plan_type"] for p in plans]
    assert "free" in plan_types
    assert "premium" in plan_types


def test_my_subscription_unauthenticated(client):
    res = client.get("/subscriptions/me")
    assert res.status_code == 401


def test_my_subscription_default_free(client, auth_headers):
    res = client.get("/subscriptions/me", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert data["plan_type"] == "free"


def test_upgrade_to_premium(client, seed_plans, auth_headers):
    res = client.post("/subscriptions/upgrade", headers=auth_headers)
    assert res.status_code == 200
    assert res.json()["plan_type"] == "premium"


def test_ai_debug_requires_premium(client, auth_headers):
    res = client.post(
        "/subscriptions/ai-debug",
        json={"code": "print('hello')", "language": "python"},
        headers=auth_headers,
    )
    # 프리미엄 미구독 상태이므로 403
    assert res.status_code == 403


def test_ai_debug_premium(client, seed_plans, auth_headers):
    # 업그레이드 먼저
    client.post("/subscriptions/upgrade", headers=auth_headers)
    res = client.post(
        "/subscriptions/ai-debug",
        json={"code": "def foo(): pass", "language": "python"},
        headers=auth_headers,
    )
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "ok"
    assert "suggestions" in data
