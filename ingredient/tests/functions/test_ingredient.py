import pytest
from fastapi import HTTPException

from ingredient.db import mongodb
from ingredient.functions.ingredient import create, get_by_id, update, delete
from ingredient.models import ModelIngredient
from ingredient.schemas.ingredient import SchemaIngredientUpdate

mongodb.connect_to_database()

ulid_test = ''


def test_create():
    global ulid_test
    ingredient_data = {
        "label": "Label test"
    }

    # création d'un appel à la méthode create
    payload = ModelIngredient(**ingredient_data)
    result = create(payload)

    # contrôle de la présence de l'id et de sa taille
    assert len(result['_id']) == 26

    # maj de la variable globale ulid_test
    ulid_test = result['_id']


def test_read():
    global ulid_test

    # création d'un appel à la méthode read correct
    result = get_by_id(ulid_test)

    # contrôle de la présence de l'id et de son contenu attendu
    assert result._id == ulid_test

    # Test an incorrect read
    with pytest.raises(HTTPException) as raise_info:
        get_by_id('TOTO')

    # Check if the error message in the exception is as expected
    assert "Ingredient 'TOTO' not found" in str(raise_info)


def test_update():
    global ulid_test
    ingredient_data = {
        "label": "new label"
    }

    # création d'un appel à la méthode update
    update(_id = ulid_test, payload = ingredient_data)

    # lecture de l'objet pour contrôle
    result = get_by_id(ulid_test)

    # contrôle de la présence des informations attendues
    assert result._id == ulid_test
    assert result.label == 'new label'


def test_delete():
    global ulid_test

    # création d'un appel à la méthode delete
    delete(ulid_test)

    # Test an incorrect read
    with pytest.raises(HTTPException) as raise_info:
        get_by_id(ulid_test)

    # Check if the error message in the exception is as expected
    assert "Ingredient '" + ulid_test + "' not found" in str(raise_info)


if __name__ == "__main__":
    pytest.main()
