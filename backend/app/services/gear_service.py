from typing import Tuple, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc, func

from ..models import Gear, GearReview
from ..models.gear import GearType
from ..repositories.base import BaseRepository
from ..core.logging import get_logger

logger = get_logger("service.gear")


class GearService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = BaseRepository(Gear, db)

    def create_gear(self, gear_data: dict) -> Gear:
        gear = Gear(**gear_data)
        logger.info(f"Creating gear: {gear_data.get('name')}")
        return self.repo.create(gear)

    def get_gears(
        self,
        page: int = 1,
        page_size: int = 12,
        gear_type: Optional[GearType] = None,
        recommended_only: bool = False,
    ) -> Tuple[List[Gear], int]:
        filters = []
        if gear_type:
            filters.append(Gear.gear_type == gear_type)
        if recommended_only:
            filters.append(Gear.is_recommended == True)
        return self.repo.get_paginated(page, page_size, filters, desc(Gear.average_rating))

    def get_recommended(self, gear_type: Optional[GearType] = None) -> List[Gear]:
        query = self.db.query(Gear).filter(Gear.is_recommended == True)
        if gear_type:
            query = query.filter(Gear.gear_type == gear_type)
        return query.order_by(desc(Gear.average_rating)).all()

    def get_gear(self, gear_id: int) -> Optional[Gear]:
        return self.repo.get_by_id(gear_id)

    def update_gear(self, gear_id: int, update_data: dict) -> Optional[Gear]:
        gear = self.repo.get_by_id(gear_id)
        if not gear:
            return None
        return self.repo.update(gear, update_data)

    def delete_gear(self, gear_id: int) -> bool:
        gear = self.repo.get_by_id(gear_id)
        if not gear:
            return False
        self.repo.delete(gear)
        return True

    def create_review(self, gear_id: int, user_id: int, review_data: dict) -> Optional[GearReview]:
        gear = self.repo.get_by_id(gear_id)
        if not gear:
            return None
        existing = (
            self.db.query(GearReview)
            .filter(GearReview.gear_id == gear_id, GearReview.user_id == user_id)
            .first()
        )
        if existing:
            return "exists"
        review = GearReview(gear_id=gear_id, user_id=user_id, **review_data)
        self.db.add(review)
        self._recalc_rating(gear)
        gear.review_count += 1
        self.db.commit()
        self.db.refresh(review)
        return review

    def get_reviews(self, gear_id: int, page: int = 1, page_size: int = 12) -> Tuple[List[GearReview], int]:
        repo = BaseRepository(GearReview, self.db)
        filters = [GearReview.gear_id == gear_id]
        return repo.get_paginated(page, page_size, filters, desc(GearReview.created_at))

    def update_review(self, review_id: int, user_id: int, update_data: dict) -> Optional[GearReview]:
        review = (
            self.db.query(GearReview)
            .filter(GearReview.id == review_id, GearReview.user_id == user_id)
            .first()
        )
        if not review:
            return None
        old_rating = review.rating
        for field, value in update_data.items():
            setattr(review, field, value)
        if "rating" in update_data and update_data["rating"] != old_rating:
            gear = self.repo.get_by_id(review.gear_id)
            self._recalc_rating(gear)
        self.db.commit()
        self.db.refresh(review)
        return review

    def delete_review(self, review_id: int, user_id: int) -> bool:
        review = (
            self.db.query(GearReview)
            .filter(GearReview.id == review_id, GearReview.user_id == user_id)
            .first()
        )
        if not review:
            return False
        gear_id = review.gear_id
        self.db.delete(review)
        gear = self.repo.get_by_id(gear_id)
        self._recalc_rating(gear)
        gear.review_count = max(0, gear.review_count - 1)
        self.db.commit()
        return True

    def _recalc_rating(self, gear: Gear):
        avg = (
            self.db.query(func.avg(GearReview.rating))
            .filter(GearReview.gear_id == gear.id)
            .scalar()
        )
        gear.average_rating = round(avg, 2) if avg else 0.0
