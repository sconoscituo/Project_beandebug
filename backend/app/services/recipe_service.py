from typing import Tuple, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc

from ..models import Recipe, Bean, RecipeComment, RecipeLike
from ..repositories.base import BaseRepository
from ..core.logging import get_logger

logger = get_logger("service.recipe")


class RecipeService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = BaseRepository(Recipe, db)

    def create_recipe(self, recipe_data: dict, owner_id: int) -> Optional[Recipe]:
        bean = (
            self.db.query(Bean)
            .filter(
                Bean.id == recipe_data.get("bean_id"),
                or_(Bean.owner_id == owner_id, Bean.is_public == True),
            )
            .first()
        )
        if not bean:
            return None
        recipe = Recipe(**recipe_data, owner_id=owner_id)
        logger.info(f"Creating recipe: {recipe_data.get('title')} for user {owner_id}")
        return self.repo.create(recipe)

    def get_my_recipes(
        self, owner_id: int, page: int = 1, page_size: int = 12, bean_id: Optional[int] = None
    ) -> Tuple[List[Recipe], int]:
        filters = [Recipe.owner_id == owner_id]
        if bean_id:
            filters.append(Recipe.bean_id == bean_id)
        return self.repo.get_paginated(page, page_size, filters)

    def get_public_recipes(
        self,
        page: int = 1,
        page_size: int = 12,
        brew_method: Optional[str] = None,
        sort_by: str = "recent",
    ) -> Tuple[List[Recipe], int]:
        filters = [Recipe.is_public == True]
        if brew_method:
            filters.append(Recipe.brew_method == brew_method)

        order = {
            "popular": desc(Recipe.likes_count),
            "rating": desc(Recipe.overall_rating),
        }.get(sort_by, desc(Recipe.created_at))

        return self.repo.get_paginated(page, page_size, filters, order)

    def get_recipe(self, recipe_id: int, user_id: Optional[int] = None) -> Optional[Recipe]:
        query = self.db.query(Recipe).filter(Recipe.id == recipe_id)
        if user_id:
            query = query.filter(
                or_(Recipe.owner_id == user_id, Recipe.is_public == True)
            )
        else:
            query = query.filter(Recipe.is_public == True)
        recipe = query.first()
        if recipe and (not user_id or recipe.owner_id != user_id):
            recipe.view_count += 1
            self.db.commit()
        return recipe

    def update_recipe(self, recipe_id: int, owner_id: int, update_data: dict) -> Optional[Recipe]:
        recipe = (
            self.db.query(Recipe)
            .filter(Recipe.id == recipe_id, Recipe.owner_id == owner_id)
            .first()
        )
        if not recipe:
            return None
        if "bean_id" in update_data:
            bean = (
                self.db.query(Bean)
                .filter(
                    Bean.id == update_data["bean_id"],
                    or_(Bean.owner_id == owner_id, Bean.is_public == True),
                )
                .first()
            )
            if not bean:
                return None
        return self.repo.update(recipe, update_data)

    def delete_recipe(self, recipe_id: int, owner_id: int) -> bool:
        recipe = (
            self.db.query(Recipe)
            .filter(Recipe.id == recipe_id, Recipe.owner_id == owner_id)
            .first()
        )
        if not recipe:
            return False
        self.repo.delete(recipe)
        return True

    def like_recipe(self, recipe_id: int, user_id: int) -> Optional[str]:
        recipe = self.db.query(Recipe).filter(Recipe.id == recipe_id, Recipe.is_public == True).first()
        if not recipe:
            return "not_found"
        existing = (
            self.db.query(RecipeLike)
            .filter(RecipeLike.recipe_id == recipe_id, RecipeLike.user_id == user_id)
            .first()
        )
        if existing:
            return "already_liked"
        self.db.add(RecipeLike(recipe_id=recipe_id, user_id=user_id))
        recipe.likes_count += 1
        self.db.commit()
        return None

    def unlike_recipe(self, recipe_id: int, user_id: int) -> bool:
        like = (
            self.db.query(RecipeLike)
            .filter(RecipeLike.recipe_id == recipe_id, RecipeLike.user_id == user_id)
            .first()
        )
        if not like:
            return False
        self.db.delete(like)
        recipe = self.db.query(Recipe).filter(Recipe.id == recipe_id).first()
        if recipe:
            recipe.likes_count = max(0, recipe.likes_count - 1)
        self.db.commit()
        return True

    def create_comment(self, recipe_id: int, user_id: int, content: str, parent_id: Optional[int] = None) -> Optional[RecipeComment]:
        recipe = self.db.query(Recipe).filter(Recipe.id == recipe_id, Recipe.is_public == True).first()
        if not recipe:
            return None
        comment = RecipeComment(
            content=content, recipe_id=recipe_id, user_id=user_id, parent_id=parent_id
        )
        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)
        return comment

    def get_comments(self, recipe_id: int) -> List[RecipeComment]:
        return (
            self.db.query(RecipeComment)
            .filter(RecipeComment.recipe_id == recipe_id)
            .order_by(RecipeComment.created_at)
            .all()
        )
