from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from ..database.connection import Base

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(Text)
    bean_id = Column(Integer, ForeignKey("beans.id"))

    brew_method = Column(String)
    grind_size = Column(String)
    water_temp = Column(Float)
    coffee_amount = Column(Float)
    water_amount = Column(Float)
    brew_time = Column(Integer)
    ratio = Column(String)

    steps = Column(Text)
    tips = Column(Text)

    taste_rating = Column(Integer)
    body_rating = Column(Integer)
    acidity_rating = Column(Integer)
    sweetness_rating = Column(Integer)
    overall_rating = Column(Float)
    notes = Column(Text)

    is_public = Column(Boolean, default=False)
    view_count = Column(Integer, default=0)
    likes_count = Column(Integer, default=0)

    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    owner = relationship("User", back_populates="recipes")
    bean = relationship("Bean", back_populates="recipes")
    comments = relationship("RecipeComment", back_populates="recipe", cascade="all, delete-orphan")
    likes = relationship("RecipeLike", back_populates="recipe", cascade="all, delete-orphan")
    featured = relationship("FeaturedRecipe", back_populates="recipe")
