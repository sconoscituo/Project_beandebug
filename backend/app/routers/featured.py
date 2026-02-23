from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from ..database.connection import get_db
from ..models import BeanOfTheMonth, FeaturedRecipe, Bean, Recipe, User
from ..schemas import (
    BeanOfTheMonthCreate,
    BeanOfTheMonthResponse,
    FeaturedRecipeCreate,
    FeaturedRecipeResponse
)
from ..utils.auth import get_current_admin_user

router = APIRouter(prefix="/featured", tags=["Featured Content"])

@router.post("/bean-of-month", response_model=BeanOfTheMonthResponse, status_code=status.HTTP_201_CREATED)
def create_bean_of_month(
    bean_of_month: BeanOfTheMonthCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    bean = db.query(Bean).filter(Bean.id == bean_of_month.bean_id).first()
    if not bean:
        raise HTTPException(status_code=404, detail="Bean not found")
    existing = db.query(BeanOfTheMonth).filter(
        BeanOfTheMonth.month == bean_of_month.month
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Bean of the month already exists for this month")
    db_bean_of_month = BeanOfTheMonth(**bean_of_month.model_dump())
    db.add(db_bean_of_month)
    db.commit()
    db.refresh(db_bean_of_month)
    return db_bean_of_month

@router.get("/bean-of-month/current", response_model=BeanOfTheMonthResponse)
def get_current_bean_of_month(db: Session = Depends(get_db)):
    current_month = datetime.now(timezone.utc).strftime("%Y-%m")
    bean_of_month = db.query(BeanOfTheMonth).filter(
        BeanOfTheMonth.month == current_month,
        BeanOfTheMonth.is_active == True
    ).first()
    if not bean_of_month:
        raise HTTPException(status_code=404, detail="No bean of the month for current month")
    return bean_of_month

@router.get("/bean-of-month", response_model=List[BeanOfTheMonthResponse])
def get_beans_of_month(
    skip: int = 0,
    limit: int = 12,
    db: Session = Depends(get_db)
):
    return db.query(BeanOfTheMonth).filter(
        BeanOfTheMonth.is_active == True
    ).order_by(BeanOfTheMonth.month.desc()).offset(skip).limit(limit).all()

@router.post("/recipes", response_model=FeaturedRecipeResponse, status_code=status.HTTP_201_CREATED)
def create_featured_recipe(
    featured: FeaturedRecipeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    recipe = db.query(Recipe).filter(Recipe.id == featured.recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    db_featured = FeaturedRecipe(**featured.model_dump())
    db.add(db_featured)
    db.commit()
    db.refresh(db_featured)
    return db_featured

@router.get("/recipes", response_model=List[FeaturedRecipeResponse])
def get_featured_recipes(
    category: str = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    query = db.query(FeaturedRecipe).filter(FeaturedRecipe.is_active == True)
    if category:
        query = query.filter(FeaturedRecipe.category == category)
    now = datetime.now(timezone.utc)
    query = query.filter(
        (FeaturedRecipe.expires_at.is_(None)) | (FeaturedRecipe.expires_at > now)
    )
    return query.order_by(
        FeaturedRecipe.display_order,
        FeaturedRecipe.created_at.desc()
    ).offset(skip).limit(limit).all()
