from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from ..database.connection import get_db
from ..models import Bean, User
from ..schemas import BeanCreate, BeanUpdate, BeanResponse
from ..utils.auth import get_current_active_user

router = APIRouter(prefix="/beans", tags=["Beans"])

@router.post("/", response_model=BeanResponse, status_code=status.HTTP_201_CREATED)
def create_bean(
    bean: BeanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """원두 등록"""
    db_bean = Bean(**bean.dict(), owner_id=current_user.id)
    db.add(db_bean)
    db.commit()
    db.refresh(db_bean)
    return db_bean

@router.get("/", response_model=List[BeanResponse])
def get_my_beans(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """내 원두 목록"""
    beans = db.query(Bean).filter(Bean.owner_id == current_user.id).offset(skip).limit(limit).all()
    return beans

@router.get("/public", response_model=List[BeanResponse])
def get_public_beans(
    skip: int = 0,
    limit: int = 100,
    origin: str = Query(None),
    roast_level: str = Query(None),
    db: Session = Depends(get_db)
):
    """공개된 원두 목록"""
    query = db.query(Bean).filter(Bean.is_public == True)
    
    if origin:
        query = query.filter(Bean.origin.ilike(f"%{origin}%"))
    if roast_level:
        query = query.filter(Bean.roast_level == roast_level)
    
    beans = query.offset(skip).limit(limit).all()
    return beans

@router.get("/{bean_id}", response_model=BeanResponse)
def get_bean(
    bean_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """원두 상세 조회"""
    bean = db.query(Bean).filter(
        Bean.id == bean_id,
        or_(Bean.owner_id == current_user.id, Bean.is_public == True)
    ).first()
    
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
    """원두 정보 수정"""
    bean = db.query(Bean).filter(Bean.id == bean_id, Bean.owner_id == current_user.id).first()
    if not bean:
        raise HTTPException(status_code=404, detail="Bean not found")
    
    update_data = bean_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(bean, field, value)
    
    db.commit()
    db.refresh(bean)
    return bean

@router.delete("/{bean_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bean(
    bean_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """원두 삭제"""
    bean = db.query(Bean).filter(Bean.id == bean_id, Bean.owner_id == current_user.id).first()
    if not bean:
        raise HTTPException(status_code=404, detail="Bean not found")
    
    db.delete(bean)
    db.commit()
    return None