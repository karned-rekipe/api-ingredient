from typing import List

from fastapi import APIRouter, status, Query, Body
from icecream import ic
from ingredient.config import *
from ingredient.libs.responses import responses_default, responses_healthcheck

from ingredient.libs.docs import *

router = APIRouter(
    responses = responses_default
)


@router.get("/healthchecker/",
            name = "Simple healthcheck",
            summary = "Simple healthcheck",
            description = "Simple healthcheck",
            response_description = "Confirmation message",
            responses = responses_healthcheck,
            status_code = status.HTTP_200_OK)
async def healthcheck():
    """ Healthcheck
    """
    message = 'API /v' + api_v + '/' + api + ' is LIVE!'
    return {"message": message}


@router.get("/pebbledocs/",
            name = "Pebble Docs",
            summary = "Pebble Docs",
            description = "Pebble Docs",
            response_description = "Pebble Docs",
            responses = responses_default,
            status_code = status.HTTP_200_OK,
            include_in_schema=False)
async def pebble_docs():
    """ Pebble Docs
    """
    return get_swagger_ui_html(
        openapi_url = '/v' + api_v + '/' + api + '/openapi.json',
        title = "Pebble Docs " + '/v' + api_v + '/' + api,
    )