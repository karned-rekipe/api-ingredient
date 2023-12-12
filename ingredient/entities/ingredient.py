from typing import Union

from icecream import ic
from datetime import datetime
from fastapi import HTTPException, status

from ingredient.models.ingredient import ModelIngredient


class Ingredient:
    DB_DBMS = 'MongoDB'
    DB_CONTAINER = 'ingredient'

    def __init__(self, ingredient: Union[ModelIngredient, dict]):
        if isinstance(ingredient, ModelIngredient):
            self._id: str = ingredient.id
            self.label: str = ingredient.label
            self.start: datetime = ingredient.start
            self.end: datetime = ingredient.end
        elif isinstance(ingredient, dict):
            self._id: str = ingredient.get('id')
            self.label: str = ingredient.get('label')
            self.start: datetime = ingredient.get('start')
            self.end: datetime = ingredient.get('end')
        else:
            raise HTTPException(
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail = {
                    "message": "Invalid ingredient type. Expected ModelIngredient or dict."
                }
            )

        self.status: str = self.get_status()

    def get_status(self, date=None) -> str:
        if date is None:
            reference = datetime.now().date()
        else:
            reference = datetime.strptime(date, '%Y-%m-%d').date()

        start = self.start.date() if self.start is not None else None
        end = self.end.date() if self.end is not None else None

        if date is not None:
            reference = date

        if start is None and end is None:
            return "Active"
        elif start is not None and end is None:
            return "Active" if start <= reference else "Inactive"
        elif start is None and end is not None:
            return "Active" if end >= reference else "Inactive"
        elif start is not None and end is not None:
            return "Active" if start <= reference <= end else "Inactive"

        return 'Inactive'
