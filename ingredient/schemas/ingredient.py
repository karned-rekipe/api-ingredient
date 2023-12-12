from ingredient.models import *


class HealthcheckResponse(BaseModel):
    message: str


class SchemaIngredientId(ModelIngredientUlid):
    """Ingredient ID schema
    """
    pass


class SchemaIngredientCreate(ModelIngredientDatabaseFields, ModelIngredientUlidOptional):
    """Create ingredient schema
    """
    pass


class SchemaIngredientRead(ModelIngredientComputeFields, ModelIngredientDatabaseFields, ModelIngredientUlid):
    """Read ingredient schema
    """
    pass


class SchemaIngredientUpdate(ModelIngredientDatabaseFields):
    """Update ingredient schema
    """
    pass
