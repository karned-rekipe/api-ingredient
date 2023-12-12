import pytest
import requests

from ingredient.config import api_v, api, test_server, test_port

API_BASE_URL = test_server + ":" + test_port + "/v" + api_v + "/" + api

ulid_test = ''


def test_post_ingredient():
    global ulid_test
    ingredient_data = {
        "label": "Label test"
    }
    response = requests.post(f"{API_BASE_URL}/", json = ingredient_data)
    assert response.status_code == 201
    updated_ingredient_data = response.json()

    # maj de la variable globale ulid_test
    ulid_test = updated_ingredient_data["_id"]


def test_get_ingredient():
    response = requests.get(f"{API_BASE_URL}/")
    assert response.status_code == 200
    # ingredient_data = response.json()
    # assert ingredient_data["name"] == "John Doe"


def test_get_ingredient_by_ulid():
    global ulid_test
    response = requests.get(f"{API_BASE_URL}/" + ulid_test + "/")
    assert response.status_code == 200
    ingredient_data = response.json()
    assert ingredient_data["label"] == "Label test"


def test_get_ingredient_by_ulid_wrong():
    response = requests.get(f"{API_BASE_URL}/TOTO/")
    assert response.status_code == 404


def test_patch_ingredient():
    ingredient_data = {
        "label": "Label new"
    }
    response = requests.patch(f"{API_BASE_URL}/" + ulid_test + "/", json = ingredient_data)
    assert response.status_code == 204

    response = requests.get(f"{API_BASE_URL}/" + ulid_test + "/")
    assert response.status_code == 200
    ingredient_data = response.json()
    assert ingredient_data["label"] == "Label new"


def test_delete_ingredient():
    global ulid_test
    response = requests.delete(f"{API_BASE_URL}/" + ulid_test + "/")
    assert response.status_code == 202

    response = requests.get(f"{API_BASE_URL}/" + ulid_test + "/")
    assert response.status_code == 404

if __name__ == "__main__":
    pytest.main()
