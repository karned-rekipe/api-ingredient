import logging
import os
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from icecream import ic

from ingredient.config import *
from ingredient.db import mongodb
from ingredient.routers import ingredient, devops

ic.configureOutput(prefix = 'ic| -> ')

logging.basicConfig(level = logging.DEBUG)
logging.info('Start /v' + api_v + '/' + api)


@asynccontextmanager
async def lifespan(app: FastAPI):
    mongodb.connect_to_database()
    yield
    mongodb.close_database_connection()


app = FastAPI(
    lifespan = lifespan,
    title = "/ingredient",
    description = "API to manage ingredients.",
    version = "1.0.1",
    openapi_url = '/v' + api_v + '/' + api + '/openapi.json',
    docs_url = '/v' + api_v + '/' + api + '/docs',
    redoc_url = None,
    terms_of_service = "https://api.pebble.solutions/terms.html",
    contact = {
        "name": "Pebble",
        "url": "https://www.pebble.solutions",
        "email": "support@pebble.solutions",
    },
    openapi_tags = [
        {
            'name': 'ingredient',
            'description': "paths for ingredient",
            "externalDocs": {
                "description": "External docs",
                "url": "https://www.pebble.solutions",
            }
        },
        {
            'name': 'devops',
            'description': "paths for devops",
            "externalDocs": {
                "description": "External docs",
                "url": "https://www.pebble.solutions",
            }
        }
    ])

# origins = ["http://127.0.0.1:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["GET", "POST", "PUT", "DELETE"],
    allow_headers = ["*"],
)

app.include_router(ingredient.router, tags = ["ingredient"], prefix = "/v" + api_v + "/" + api)
app.include_router(devops.router, tags = ["devops"], prefix = "/v" + api_v + "/" + api)

if __name__ == "__main__" and os.environ.get("ENVIRONMENT") != "PRODUCTION":
    uvicorn.run(app, host = "127.0.0.1", port = 3000)
