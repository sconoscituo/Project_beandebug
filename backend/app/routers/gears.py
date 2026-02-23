from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, func

from ..database.connection import get_db
from ..models import Gear, GearReview, User
from ..models.gear import GearType
from ..schemas import (
    GearCreate,
    GearUpdate,
    GearResponse,
    GearReviewCreate,
    GearReviewUpdate,
    GearReviewResponse
)
from ..utils.auth import get_current_active_user, get_current_admin_user

router = APIRouter(prefix="/gears", tags=["Gears"])

@router.post("/", response_model=GearResponse, status_code=status.HTTP_201_CREATED)
def create_gear(
    gear: GearCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    db_gear = Gear(**gear.model_dump())
    db.add(db_gear)
    db.commit()
    db.refresh(db_gear)
    return db_gear

@router.get("/", response_model=List[GearResponse])
def get_gears(
    skip: int = 0,
    limit: int = 100,
    gear_type: GearType = Query(None),
    recommended_only: bool = False,
    db: Session = Depends(get_db)
):
    query = db.query(Gear)
    if gear_type:
        query = query.filter(Gear.gear_type == gear_type)
    if recommended_only:
        query = query.filter(Gear.is_recommended == True)
    gears = query.order_by(desc(Gear.average_rating)).offset(skip).limit(limit).all()
    return gears

@router.get("/recommendations", response_model=List[GearResponse])
def get_recommended_gears(
    gear_type: GearType = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Gear).filter(Gear.is_recommended == True)
    if gear_type:
        query = query.filter(Gear.gear_type == gear_type)
    gears = query.order_by(desc(Gear.average_rating)).all()
    return gears

@router.get("/{gear_id}", response_model=GearResponse)
def get_gear(
    gear_id: int,
    db: Session = Depends(get_db)
):
    gear = db.query(Gear).filter(Gear.id == gear_id).first()
    if not gear:
        raise HTTPException(status_code=404, detail="Gear not found")
    return gear

@router.put("/{gear_id}", response_model=GearResponse)
def update_gear(
    gear_id: int,
    gear_update: GearUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    gear = db.query(Gear).filter(Gear.id == gear_id).first()
    if not gear:
        raise HTTPException(status_code=404, detail="Gear not found")
    update_data = gear_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(gear, field, value)
    db.commit()
    db.refresh(gear)
    return gear

@router.delete("/{gear_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_gear(
    gear_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    gear = db.query(Gear).filter(Gear.id == gear_id).first()
    if not gear:
        raise HTTPException(status_code=404, detail="Gear not found")
    db.delete(gear)
    db.commit()
    return None

# reviews
@router.post("/{gear_id}/reviews", response_model=GearReviewResponse, status_code=status.HTTP_201_CREATED)
def create_gear_review(
    gear_id: int,
    review: GearReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    gear = db.query(Gear).filter(Gear.id == gear_id).first()
    if not gear:
        raise HTTPException(status_code=404, detail="Gear not found")

    existing_review = db.query(GearReview).filter(
        GearReview.gear_id == gear_id,
        GearReview.user_id == current_user.id
    ).first()
    if existing_review:
        raise HTTPException(status_code=400, detail="Review already exists")

    db_review = GearReview(
        gear_id=gear_id,
        user_id=current_user.id,
        **review.model_dump(exclude={'gear_id'})
    )
    db.add(db_review)

    avg_rating = db.query(func.avg(GearReview.rating)).filter(
        GearReview.gear_id == gear_id
    ).scalar()
    gear.average_rating = round(avg_rating, 2) if avg_rating else 0
    gear.review_count += 1

    db.commit()
    db.refresh(db_review)
    return db_review

@router.get("/{gear_id}/reviews", response_model=List[GearReviewResponse])
def get_gear_reviews(
    gear_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    reviews = db.query(GearReview).filter(
        GearReview.gear_id == gear_id
    ).order_by(desc(GearReview.created_at)).offset(skip).limit(limit).all()
    return reviews

@router.put("/reviews/{review_id}", response_model=GearReviewResponse)
def update_gear_review(
    review_id: int,
    review_update: GearReviewUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    review = db.query(GearReview).filter(
        GearReview.id == review_id,
        GearReview.user_id == current_user.id
    ).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    update_data = review_update.model_dump(exclude_unset=True)
    old_rating = review.rating

    for field, value in update_data.items():
        setattr(review, field, value)

    if "rating" in update_data and update_data["rating"] != old_rating:
        gear = db.query(Gear).filter(Gear.id == review.gear_id).first()
        avg_rating = db.query(func.avg(GearReview.rating)).filter(
            GearReview.gear_id == review.gear_id
        ).scalar()
        gear.average_rating = round(avg_rating, 2) if avg_rating else 0

    db.commit()
    db.refresh(review)
    return review

@router.delete("/reviews/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_gear_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    review = db.query(GearReview).filter(
        GearReview.id == review_id,
        GearReview.user_id == current_user.id
    ).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    gear_id = review.gear_id
    db.delete(review)

    gear = db.query(Gear).filter(Gear.id == gear_id).first()
    avg_rating = db.query(func.avg(GearReview.rating)).filter(
        GearReview.gear_id == gear_id
    ).scalar()
    gear.average_rating = round(avg_rating, 2) if avg_rating else 0
    gear.review_count = max(0, gear.review_count - 1)

    db.commit()
    return None
