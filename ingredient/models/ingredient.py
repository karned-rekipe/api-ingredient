from typing import Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime
import ulid


class ModelIngredientUlid(BaseModel):
    id: ulid = Field(
        default_factory = ulid.ulid,
        alias = "_id",
        description = "ULID of ingredient",
        example = "01H81Z7W545XNWSP9B4JMRMODC"
    )

    class Config:
        arbitrary_types_allowed = True


class ModelIngredientUlidOptional(BaseModel):
    id: Optional[str] = Field(
        None,
        alias = "_id",
        description = "ULID of ingredient (optional)",
        example = "01H81Z7W545XNWSP9B4JMRRRC0"
    )


class ModelIngredientDatabaseFields(BaseModel):
    label: str = Field(
        ...,
        description = "The name of my ingredient",
        example = "My ingredient name",
        min_length = 1,
        max_length = 50
    )
    start: Optional[datetime] = Field(
        None,
        description = "The date when ingredient start to be a ingredient",
        example = "2022-11-17 09:00:00"
    )
    end: Optional[datetime] = Field(
        None,
        description = "The date when ingredient stop to be a ingredient",
        example = "2023-12-31 23:59:59"
    )


class ModelIngredientComputeFields(BaseModel):
    status: str = Field(
        ...,
        description = "Status of ingredient",
        example = "Active"
    )


class ModelIngredient(ModelIngredientDatabaseFields, ModelIngredientUlid):
    pass
