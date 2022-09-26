from __future__ import annotations

from datetime import datetime
from typing import Optional, Union

from pydantic import UUID4, validator

from mealie.schema._mealie import MealieModel
from mealie.schema._mealie.types import NoneFloat
from mealie.schema.recipe.recipe_ingredient import IngredientFood, IngredientUnit
from mealie.schema.response.pagination import PaginationBase


class ShoppingListItemRecipeRef(MealieModel):
    recipe_id: UUID4
    recipe_quantity: NoneFloat

    # some recipes have a null quantity, so we default to 0
    @validator("recipe_quantity")
    def default_null_quantity(cls, v):
        return v or 0


class ShoppingListItemRecipeRefOut(ShoppingListItemRecipeRef):
    id: UUID4
    shopping_list_item_id: UUID4

    class Config:
        orm_mode = True


class ShoppingListItemCreate(MealieModel):
    shopping_list_id: UUID4
    checked: bool = False
    position: int = 0

    is_food: bool = False

    note: Optional[str] = ""
    quantity: float = 1
    unit_id: UUID4 = None
    unit: Optional[IngredientUnit]
    food_id: UUID4 = None
    food: Optional[IngredientFood]

    label_id: Optional[UUID4] = None
    recipe_references: list[ShoppingListItemRecipeRef] = []

    created_at: Optional[datetime]
    update_at: Optional[datetime]


class ShoppingListItemUpdate(ShoppingListItemCreate):
    id: UUID4


class ShoppingListItemOut(ShoppingListItemUpdate):
    label: Optional[MultiPurposeLabelSummary]
    recipe_references: list[Union[ShoppingListItemRecipeRef, ShoppingListItemRecipeRefOut]] = []

    class Config:
        orm_mode = True


class ShoppingListCreate(MealieModel):
    name: str = None

    created_at: Optional[datetime]
    update_at: Optional[datetime]


class ShoppingListRecipeRefOut(MealieModel):
    id: UUID4
    shopping_list_id: UUID4
    recipe_id: UUID4
    recipe_quantity: float
    recipe: RecipeSummary

    class Config:
        orm_mode = True


class ShoppingListSave(ShoppingListCreate):
    group_id: UUID4


class ShoppingListSummary(ShoppingListSave):
    id: UUID4

    class Config:
        orm_mode = True


class ShoppingListPagination(PaginationBase):
    items: list[ShoppingListSummary]


class ShoppingListUpdate(ShoppingListSummary):
    list_items: list[ShoppingListItemOut] = []


class ShoppingListOut(ShoppingListUpdate):
    recipe_references: list[ShoppingListRecipeRefOut]

    class Config:
        orm_mode = True


from mealie.schema.labels.multi_purpose_label import MultiPurposeLabelSummary
from mealie.schema.recipe.recipe import RecipeSummary

ShoppingListRecipeRefOut.update_forward_refs()
ShoppingListItemOut.update_forward_refs()
