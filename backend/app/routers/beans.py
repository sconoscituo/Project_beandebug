from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from ..database.connection import get_db
from ..models import User
from ..schemas import BeanCreate, BeanUpdate, BeanResponse
from ..schemas.pagination import PaginatedResponse
from ..services import BeanService
from ..utils.auth import get_current_active_user
from ..core.config import get_global_config

config = get_global_config()
router = APIRouter(prefix="/beans", tags=["Beans"])


@router.post("/", response_model=BeanResponse, status_code=status.HTTP_201_CREATED)
def create_bean(
    bean: BeanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    svc = BeanService(db)
    return svc.create_bean(bean.model_dump(), current_user.id)


@router.get("/")
def get_my_beans(
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    svc = BeanService(db)
    items, total = svc.get_my_beans(current_user.id, page, page_size)
    return PaginatedResponse.create(items, total, page, page_size)


@router.get("/public")
def get_public_beans(
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=100),
    origin: str = Query(None),
    roast_level: str = Query(None),
    db: Session = Depends(get_db)
):
    svc = BeanService(db)
    items, total = svc.get_public_beans(page, page_size, origin, roast_level)
    return PaginatedResponse.create(items, total, page, page_size)


@router.get("/{bean_id}", response_model=BeanResponse)
def get_bean(
    bean_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    svc = BeanService(db)
    bean = svc.get_bean(bean_id, current_user.id)
    if not bean:
        raise HTTPException(status_code=404, detail="Bean not found")
    return bean


@router.put("/{bean_id}", response_model=BeanResponse)
def update_bean(
    bean_id: int,
    bean_update: BeanUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    svc = BeanService(db)
    bean = svc.update_bean(bean_id, current_user.id, bean_update.model_dump(exclude_unset=True))
    if not bean:
        raise HTTPException(status_code=404, detail="Bean not found")
    return bean


@router.delete("/{bean_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bean(
    bean_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    svc = BeanService(db)
    if not svc.delete_bean(bean_id, current_user.id):
        raise HTTPException(status_code=404, detail="Bean not found")
    return None
