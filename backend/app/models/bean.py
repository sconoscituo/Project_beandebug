from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from ..database.connection import Base

class Bean(Base):
    __tablename__ = "beans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    origin = Column(String)
    farm = Column(String)
    variety = Column(String)
    roast_level = Column(String)
    processing = Column(String)
    altitude = Column(String)
    flavor_notes = Column(Text)
    tasting_notes = Column(Text)

    purchase_date = Column(DateTime)
    roast_date = Column(DateTime)
    price = Column(Float)
    vendor = Column(String)

    is_public = Column(Boolean, default=False)

    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    owner = relationship("User", back_populates="beans")
    recipes = relationship("Recipe", back_populates="bean")
    bean_of_month = relationship("BeanOfTheMonth", back_populates="bean")
