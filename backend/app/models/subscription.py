import enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from ..database.connection import Base


class PlanType(str, enum.Enum):
    free = "free"
    premium = "premium"


class SubscriptionPlan(Base):
    __tablename__ = "subscription_plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)           # e.g. "Free", "Premium"
    plan_type = Column(Enum(PlanType), nullable=False, default=PlanType.free)
    price_monthly = Column(Integer, default=0)                   # KRW
    ai_debug_enabled = Column(Boolean, default=False)
    code_review_enabled = Column(Boolean, default=False)
    max_posts_per_day = Column(Integer, default=5)               # -1 = unlimited
    description = Column(String)

    subscriptions = relationship("UserSubscription", back_populates="plan")


class UserSubscription(Base):
    __tablename__ = "user_subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    plan_id = Column(Integer, ForeignKey("subscription_plans.id"), nullable=False)
    is_active = Column(Boolean, default=True)
    started_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    expires_at = Column(DateTime, nullable=True)                 # None = indefinite (free)

    user = relationship("User", back_populates="subscription")
    plan = relationship("SubscriptionPlan", back_populates="subscriptions")
