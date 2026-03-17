from typing import TypeVar, Generic, Type, Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from ..database.connection import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db

    def get_by_id(self, id: int) -> Optional[ModelType]:
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_paginated(
        self,
        page: int = 1,
        page_size: int = 12,
        filters=None,
        order_by=None,
    ) -> Tuple[List[ModelType], int]:
        query = self.db.query(self.model)
        if filters is not None:
            for f in filters:
                query = query.filter(f)
        total = query.count()
        if order_by is not None:
            query = query.order_by(order_by)
        else:
            if hasattr(self.model, "created_at"):
                query = query.order_by(desc(self.model.created_at))
        offset = (page - 1) * page_size
        items = query.offset(offset).limit(page_size).all()
        return items, total

    def create(self, obj: ModelType) -> ModelType:
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def create_batch(self, objects: List[ModelType]) -> List[ModelType]:
        self.db.add_all(objects)
        self.db.commit()
        for obj in objects:
            self.db.refresh(obj)
        return objects

    def update(self, obj: ModelType, update_data: dict) -> ModelType:
        for field, value in update_data.items():
            setattr(obj, field, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, obj: ModelType) -> None:
        self.db.delete(obj)
        self.db.commit()

    def count(self, filters=None) -> int:
        query = self.db.query(func.count(self.model.id))
        if filters:
            for f in filters:
                query = query.filter(f)
        return query.scalar() or 0
