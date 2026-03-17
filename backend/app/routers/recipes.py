from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from ..database.connection import get_db
from ..models import User
from ..schemas import (
    RecipeCreate, RecipeUpdate, RecipeResponse,
    RecipeCommentCreate, RecipeCommentResponse
)
from ..schemas.pagination import PaginatedResponse
from ..services import RecipeService
from ..utils.auth import get_current_active_user
from ..core.config import get_global_config

config = get_global_config()
router = APIRouter(prefix="/recipes", tags=["Recipes"])


@router.post("/", response_model=RecipeResponse, status_code=status.HTTP_201_CREATED)
def create_recipe(
    recipe: RecipeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    svc = RecipeService(db)
    result = svc.create_recipe(recipe.model_dump(), current_user.id)
    if not result:
        raise HTTPException(status_code=404, detail="Bean not found")
    return result


@router.get("/")
def get_my_recipes(
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=100),
    bean_id: int = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    svc = RecipeService(db)
    items, total = svc.get_my_recipes(current_user.id, page, page_size, bean_id)
    return PaginatedResponse.create(items, total, page, page_size)


@router.get("/public")
def get_public_recipes(
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=100),
    brew_method: str = Query(None),
    sort_by: str = Query("recent", pattern="^(recent|popular|rating)$"),
    db: Session = Depends(get_db)
):
    svc = RecipeService(db)
    items, total = svc.get_public_recipes(page, page_size, brew_method, sort_by)
    return PaginatedResponse.create(items, total, page, page_size)


@router.get("/{recipe_id}", response_model=RecipeResponse)
def get_recipe(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    svc = RecipeService(db)
    recipe = svc.get_recipe(recipe_id, current_user.id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@router.put("/{recipe_id}", response_model=RecipeResponse)
def update_recipe(
    recipe_id: int,
    recipe_update: RecipeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    svc = RecipeService(db)
    recipe = svc.update_recipe(recipe_id, current_user.id, recipe_update.model_dump(exclude_unset=True))
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    svc = RecipeService(db)
    if not svc.delete_recipe(recipe_id, current_user.id):
        raise HTTPException(status_code=404, detail="Recipe not found")
    return None


@router.post("/{recipe_id}/like", status_code=status.HTTP_201_CREATED)
def like_recipe(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    svc = RecipeService(db)
    error = svc.like_recipe(recipe_id, current_user.id)
    if error == "not_found":
        raise HTTPException(status_code=404, detail="Recipe not found")
    if error == "already_liked":
        raise HTTPException(status_code=400, detail="Already liked")
    return {"message": "Recipe liked"}


@router.delete("/{recipe_id}/like", status_code=status.HTTP_204_NO_CONTENT)
def unlike_recipe(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    svc = RecipeService(db)
    if not svc.unlike_recipe(recipe_id, current_user.id):
        raise HTTPException(status_code=404, detail="Like not found")
    return None


@router.post("/{recipe_id}/comments", response_model=RecipeCommentResponse, status_code=status.HTTP_201_CREATED)
def create_recipe_comment(
    recipe_id: int,
    comment: RecipeCommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    svc = RecipeService(db)
    result = svc.create_comment(recipe_id, current_user.id, comment.content, comment.parent_id)
    if not result:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return result


@router.get("/{recipe_id}/comments", response_model=List[RecipeCommentResponse])
def get_recipe_comments(recipe_id: int, db: Session = Depends(get_db)):
    svc = RecipeService(db)
    return svc.get_comments(recipe_id)
