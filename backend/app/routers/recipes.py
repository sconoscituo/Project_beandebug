from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc

from ..database.connection import get_db
from ..models import Recipe, Bean, User, RecipeComment, RecipeLike
from ..schemas import (
    RecipeCreate,
    RecipeUpdate,
    RecipeResponse,
    RecipeCommentCreate,
    RecipeCommentResponse
)
from ..utils.auth import get_current_active_user

router = APIRouter(prefix="/recipes", tags=["Recipes"])

@router.post("/", response_model=RecipeResponse, status_code=status.HTTP_201_CREATED)
def create_recipe(
    recipe: RecipeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    bean = db.query(Bean).filter(
        Bean.id == recipe.bean_id,
        or_(Bean.owner_id == current_user.id, Bean.is_public == True)
    ).first()
    if not bean:
        raise HTTPException(status_code=404, detail="Bean not found")
    db_recipe = Recipe(**recipe.model_dump(), owner_id=current_user.id)
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

@router.get("/", response_model=List[RecipeResponse])
def get_my_recipes(
    skip: int = 0,
    limit: int = 100,
    bean_id: int = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    query = db.query(Recipe).filter(Recipe.owner_id == current_user.id)
    if bean_id:
        query = query.filter(Recipe.bean_id == bean_id)
    return query.offset(skip).limit(limit).all()

@router.get("/public", response_model=List[RecipeResponse])
def get_public_recipes(
    skip: int = 0,
    limit: int = 100,
    brew_method: str = Query(None),
    sort_by: str = Query("recent", pattern="^(recent|popular|rating)$"),
    db: Session = Depends(get_db)
):
    query = db.query(Recipe).filter(Recipe.is_public == True)
    if brew_method:
        query = query.filter(Recipe.brew_method == brew_method)
    if sort_by == "popular":
        query = query.order_by(desc(Recipe.likes_count))
    elif sort_by == "rating":
        query = query.order_by(desc(Recipe.overall_rating))
    else:
        query = query.order_by(desc(Recipe.created_at))
    return query.offset(skip).limit(limit).all()

@router.get("/{recipe_id}", response_model=RecipeResponse)
def get_recipe(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    recipe = db.query(Recipe).filter(
        Recipe.id == recipe_id,
        or_(Recipe.owner_id == current_user.id, Recipe.is_public == True)
    ).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    if recipe.owner_id != current_user.id:
        recipe.view_count += 1
        db.commit()
    return recipe

@router.put("/{recipe_id}", response_model=RecipeResponse)
def update_recipe(
    recipe_id: int,
    recipe_update: RecipeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id, Recipe.owner_id == current_user.id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    update_data = recipe_update.model_dump(exclude_unset=True)
    if "bean_id" in update_data:
        bean = db.query(Bean).filter(
            Bean.id == update_data["bean_id"],
            or_(Bean.owner_id == current_user.id, Bean.is_public == True)
        ).first()
        if not bean:
            raise HTTPException(status_code=404, detail="Bean not found")
    for field, value in update_data.items():
        setattr(recipe, field, value)
    db.commit()
    db.refresh(recipe)
    return recipe

@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id, Recipe.owner_id == current_user.id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    db.delete(recipe)
    db.commit()
    return None

@router.post("/{recipe_id}/like", status_code=status.HTTP_201_CREATED)
def like_recipe(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id, Recipe.is_public == True).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    existing_like = db.query(RecipeLike).filter(
        RecipeLike.recipe_id == recipe_id,
        RecipeLike.user_id == current_user.id
    ).first()
    if existing_like:
        raise HTTPException(status_code=400, detail="Already liked")
    db.add(RecipeLike(recipe_id=recipe_id, user_id=current_user.id))
    recipe.likes_count += 1
    db.commit()
    return {"message": "Recipe liked"}

@router.delete("/{recipe_id}/like", status_code=status.HTTP_204_NO_CONTENT)
def unlike_recipe(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    like = db.query(RecipeLike).filter(
        RecipeLike.recipe_id == recipe_id,
        RecipeLike.user_id == current_user.id
    ).first()
    if not like:
        raise HTTPException(status_code=404, detail="Like not found")
    db.delete(like)
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if recipe:
        recipe.likes_count = max(0, recipe.likes_count - 1)
    db.commit()
    return None

@router.post("/{recipe_id}/comments", response_model=RecipeCommentResponse, status_code=status.HTTP_201_CREATED)
def create_recipe_comment(
    recipe_id: int,
    comment: RecipeCommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id, Recipe.is_public == True).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    db_comment = RecipeComment(
        content=comment.content,
        recipe_id=recipe_id,
        user_id=current_user.id,
        parent_id=comment.parent_id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

@router.get("/{recipe_id}/comments", response_model=List[RecipeCommentResponse])
def get_recipe_comments(
    recipe_id: int,
    db: Session = Depends(get_db)
):
    return db.query(RecipeComment).filter(
        RecipeComment.recipe_id == recipe_id
    ).order_by(RecipeComment.created_at).all()
