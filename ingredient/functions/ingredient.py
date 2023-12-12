import re

from fastapi import HTTPException, status

from ingredient.db import mongodb
from ingredient.models import ModelIngredient
from ingredient.entities import Ingredient


def get_all(_id: str, label: str) -> list[Ingredient]:
    query = {}
    if _id:
        query['_id'] = {"$regex": f'.*{re.escape(_id)}.*'}

    if label:
        query['label'] = {"$regex": f'.*{re.escape(label)}.*'}

    ingredients_data = mongodb.list(Ingredient.DB_CONTAINER, query)

    if ingredients_data is None:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = {
                "message": "An error occurred while get list of ingredients",
                "doc": "http://127.0.0.1:8000/v5/ingredient/docs#/Ingredient/Ingredients_list_v5_ingredient__get"
            })

    ingredients = [Ingredient(ModelIngredient(**ingredient_data)) for ingredient_data in ingredients_data]

    return ingredients


def get_by_id(_id: str) -> Ingredient:
    ingredient = mongodb.read(Ingredient.DB_CONTAINER, {"_id": _id})

    if ingredient is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = {
                "message": f"Ingredient '{_id}' not found",
                "doc": "http://127.0.0.1:8000/v5/ingredient/docs#/Ingredient/Get_a_ingredient_v5_ingredient__id__get"
            })

    ingredient_resp = Ingredient(ModelIngredient(**ingredient))

    return ingredient_resp


def create(payload: ModelIngredient):
    ingredient_id = mongodb.create(Ingredient.DB_CONTAINER, payload.model_dump())

    if ingredient_id is None:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = {
                "message": "Sorry, something happen during the ingredient creation"
            }
        )

    return ingredient_id


def update(payload: dict, _id: str):
    get_by_id(_id)

    ingredient_update = mongodb.update(Ingredient.DB_CONTAINER, {"_id": _id}, {"$set": payload})

    if ingredient_update is None:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = {
                "message": "Sorry, something happen during the ingredient update"
            }
        )

    return None


def delete(_id: str):
    get_by_id(_id)

    mongodb.delete(Ingredient.DB_CONTAINER, {"_id": _id})
    return None
