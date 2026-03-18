from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database.connection import Base

class BeanOfTheMonth(Base):
    __tablename__ = "bean_of_the_month"

    id = Column(Integer, primary_key=True, index=True)
    bean_id = Column(Integer, ForeignKey("beans.id"))
    month = Column(String, nullable=False, unique=True)
    title = Column(String)
    description = Column(Text)
    highlight = Column(Text)
    image_url = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    bean = relationship("Bean", back_populates="bean_of_month")

class FeaturedRecipe(Base):
    __tablename__ = "featured_recipes"

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    category = Column(String)
    title = Column(String)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    display_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    expires_at = Column(DateTime)

    recipe = relationship("Recipe", back_populates="featured")
