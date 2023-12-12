from typing import List

from fastapi import APIRouter, status, Query, Body, Depends
from fastapi.security import HTTPBearer
from icecream import ic
from ingredient.config import *
from ingredient.libs.responses import responses_update, responses_delete, responses_default
from ingredient.schemas.ingredient import (SchemaIngredientCreate, SchemaIngredientId, SchemaIngredientRead,
                                   SchemaIngredientUpdate, ModelIngredientComputeFields)
from ingredient.functions.ingredient import *

security = HTTPBearer()

router = APIRouter(
    responses = responses_default,
    dependencies=[Depends(security)]
)


@router.get("/",
            summary = "List ingredient",
            description = "Return a list of ingredients",
            response_description = "List of ingredient",
            response_model = list[SchemaIngredientRead],
            status_code = status.HTTP_200_OK)
async def list_ingredient(
        _id: str = Query(None, description = "Optional id query"),
        label: str = Query(None, description = "Optional name query")
) -> list[Ingredient]:
    """ Get a list of ingredients
    """
    ingredients = get_all(_id, label)
    return ingredients


@router.post("/",
             summary = "Create ingredient",
             description = "Create a new ingredient",
             response_description = "UILD of the created ingredient",
             response_model = SchemaIngredientId,
             status_code = status.HTTP_201_CREATED)
async def post_ingredient(payload: SchemaIngredientCreate = Body(...)) -> SchemaIngredientId:
    """ Create a new ingredient
    """
    ingredient_id = create(ModelIngredient(**payload.model_dump()))
    return ingredient_id


@router.get("/{_id}",
            summary = "Read ingredient",
            description = "Get ingredient by ulid",
            response_description = "Ingredient",
            response_model = SchemaIngredientRead)
async def get_ingredient(_id: str) -> Ingredient:
    """ Get information about a ingredient
    """
    ingredient = get_by_id(_id)
    return ingredient


@router.patch("/{_id}",
              summary = "Update ingredient",
              description = "Update ingredient",
              response_description = "status code",
              responses = responses_update,
              status_code = status.HTTP_204_NO_CONTENT)
async def update_ingredient(_id: str, payload: SchemaIngredientUpdate = Body(...)) -> None:
    """ Update a ingredient
    """
    update(payload.model_dump(), _id)
    return None


@router.delete("/{_id}",
               summary = "Delete ingredient",
               description = "Delete ingredient by ulid",
               response_description = "status code",
               responses = responses_delete,
               status_code = status.HTTP_202_ACCEPTED)
async def delete_ingredient(_id: str) -> None:
    """ Delete a ingredient
    """
    delete(_id)
    return None
