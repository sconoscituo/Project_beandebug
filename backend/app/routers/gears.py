from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from ..database.connection import get_db
from ..models import User
from ..models.gear import GearType
from ..schemas import (
    GearCreate, GearUpdate, GearResponse,
    GearReviewCreate, GearReviewUpdate, GearReviewResponse
)
from ..schemas.pagination import PaginatedResponse
from ..services import GearService
from ..utils.auth import get_current_active_user, get_current_admin_user

router = APIRouter(prefix="/gears", tags=["Gears"])


@router.post("/", response_model=GearResponse, status_code=status.HTTP_201_CREATED)
def create_gear(
    gear: GearCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    svc = GearService(db)
    return svc.create_gear(gear.model_dump())


@router.get("/")
def get_gears(
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=100),
    gear_type: GearType = Query(None),
    recommended_only: bool = False,
    db: Session = Depends(get_db)
):
    svc = GearService(db)
    items, total = svc.get_gears(page, page_size, gear_type, recommended_only)
    return PaginatedResponse.create(items, total, page, page_size)


@router.get("/recommendations", response_model=List[GearResponse])
def get_recommended_gears(
    gear_type: GearType = Query(None),
    db: Session = Depends(get_db)
):
    svc = GearService(db)
    return svc.get_recommended(gear_type)


@router.get("/{gear_id}", response_model=GearResponse)
def get_gear(gear_id: int, db: Session = Depends(get_db)):
    svc = GearService(db)
    gear = svc.get_gear(gear_id)
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
    svc = GearService(db)
    gear = svc.update_gear(gear_id, gear_update.model_dump(exclude_unset=True))
    if not gear:
        raise HTTPException(status_code=404, detail="Gear not found")
    return gear


@router.delete("/{gear_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_gear(
    gear_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    svc = GearService(db)
    if not svc.delete_gear(gear_id):
        raise HTTPException(status_code=404, detail="Gear not found")
    return None


@router.post("/{gear_id}/reviews", response_model=GearReviewResponse, status_code=status.HTTP_201_CREATED)
def create_gear_review(
    gear_id: int,
    review: GearReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    svc = GearService(db)
    result = svc.create_review(gear_id, current_user.id, review.model_dump(exclude={'gear_id'}))
    if result is None:
        raise HTTPException(status_code=404, detail="Gear not found")
    if result == "exists":
        raise HTTPException(status_code=400, detail="Review already exists")
    return result


@router.get("/{gear_id}/reviews")
def get_gear_reviews(
    gear_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=100),
    db: Session = Depends(get_db)
):
    svc = GearService(db)
    items, total = svc.get_reviews(gear_id, page, page_size)
    return PaginatedResponse.create(items, total, page, page_size)


@router.put("/reviews/{review_id}", response_model=GearReviewResponse)
def update_gear_review(
    review_id: int,
    review_update: GearReviewUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    svc = GearService(db)
    review = svc.update_review(review_id, current_user.id, review_update.model_dump(exclude_unset=True))
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review


@router.delete("/reviews/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_gear_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    svc = GearService(db)
    if not svc.delete_review(review_id, current_user.id):
        raise HTTPException(status_code=404, detail="Review not found")
    return None
