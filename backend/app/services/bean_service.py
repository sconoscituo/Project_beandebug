from typing import Tuple, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_

from ..models import Bean, User
from ..repositories.base import BaseRepository
from ..core.logging import get_logger

logger = get_logger("service.bean")


class BeanService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = BaseRepository(Bean, db)

    def create_bean(self, bean_data: dict, owner_id: int) -> Bean:
        bean = Bean(**bean_data, owner_id=owner_id)
        logger.info(f"Creating bean: {bean_data.get('name')} for user {owner_id}")
        return self.repo.create(bean)

    def get_my_beans(
        self, owner_id: int, page: int = 1, page_size: int = 12
    ) -> Tuple[List[Bean], int]:
        filters = [Bean.owner_id == owner_id]
        return self.repo.get_paginated(page, page_size, filters)

    def get_public_beans(
        self,
        page: int = 1,
        page_size: int = 12,
        origin: Optional[str] = None,
        roast_level: Optional[str] = None,
    ) -> Tuple[List[Bean], int]:
        filters = [Bean.is_public == True]
        if origin:
            filters.append(Bean.origin.ilike(f"%{origin}%"))
        if roast_level:
            filters.append(Bean.roast_level == roast_level)
        return self.repo.get_paginated(page, page_size, filters)

    def get_bean(self, bean_id: int, user_id: Optional[int] = None) -> Optional[Bean]:
        if user_id:
            return (
                self.db.query(Bean)
                .filter(
                    Bean.id == bean_id,
                    or_(Bean.owner_id == user_id, Bean.is_public == True),
                )
                .first()
            )
        return self.db.query(Bean).filter(Bean.id == bean_id, Bean.is_public == True).first()

    def update_bean(self, bean_id: int, owner_id: int, update_data: dict) -> Optional[Bean]:
        bean = (
            self.db.query(Bean)
            .filter(Bean.id == bean_id, Bean.owner_id == owner_id)
            .first()
        )
        if not bean:
            return None
        logger.info(f"Updating bean {bean_id}")
        return self.repo.update(bean, update_data)

    def delete_bean(self, bean_id: int, owner_id: int) -> bool:
        bean = (
            self.db.query(Bean)
            .filter(Bean.id == bean_id, Bean.owner_id == owner_id)
            .first()
        )
        if not bean:
            return False
        logger.info(f"Deleting bean {bean_id}")
        self.repo.delete(bean)
        return True
