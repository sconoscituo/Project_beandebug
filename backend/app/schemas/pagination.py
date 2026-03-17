from pydantic import BaseModel
from typing import Generic, TypeVar, List

T = TypeVar("T")


class PaginationParams(BaseModel):
    page: int = 1
    page_size: int = 12


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int

    @classmethod
    def create(cls, items: List[T], total: int, page: int, page_size: int):
        total_pages = max(1, (total + page_size - 1) // page_size)
        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
        )
