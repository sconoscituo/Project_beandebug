from pydantic import BaseModel
from typing import Any, List


class PaginationParams(BaseModel):
    page: int = 1
    page_size: int = 12


class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    page_size: int
    total_pages: int

    model_config = {"from_attributes": True}

    @classmethod
    def create(cls, items, total: int, page: int, page_size: int):
        total_pages = max(1, (total + page_size - 1) // page_size)
        return cls(
            items=[_serialize(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
        )


def _serialize(obj):
    if hasattr(obj, "__dict__"):
        data = {}
        for key, value in obj.__dict__.items():
            if not key.startswith("_"):
                data[key] = value
        return data
    return obj
