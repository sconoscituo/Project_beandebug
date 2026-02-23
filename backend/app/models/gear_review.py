from sqlalchemy import Column, Integer, ForeignKey, DateTime, Text, Float, String
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from ..database.connection import Base

class GearReview(Base):
    __tablename__ = "gear_reviews"

    id = Column(Integer, primary_key=True, index=True)
    gear_id = Column(Integer, ForeignKey("gears.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    rating = Column(Float, nullable=False)
    title = Column(String)
    content = Column(Text)
    pros = Column(Text)
    cons = Column(Text)

    usage_duration = Column(String)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    gear = relationship("Gear", back_populates="reviews")
    user = relationship("User", back_populates="gear_reviews")
