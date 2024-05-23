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
logging.info('Start /' + api)


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
    openapi_url = '/' + api + '/openapi.json',
    docs_url = '/' + api + '/docs',
    redoc_url = None,
    terms_of_service = "https://api.koden.bzh/terms.html",
    contact = {
        "name": "Koden",
        "url": "https://www.koden.bzh",
        "email": "support@koden.bzh",
    },
    openapi_tags = [
        {
            'name': 'ingredient',
            'description': "paths for ingredient",
            "externalDocs": {
                "description": "External docs",
                "url": "https://www.koden.bzh",
            }
        },
        {
            'name': 'devops',
            'description': "paths for devops",
            "externalDocs": {
                "description": "External docs",
                "url": "https://www.koden.bzh",
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

app.include_router(ingredient.router, tags = ["ingredient"], prefix = "/" + api)
app.include_router(devops.router, tags = ["devops"], prefix = "/" + api)

if __name__ == "__main__" and os.environ.get("ENVIRONMENT") != "PRODUCTION":
    uvicorn.run(app, host = "127.0.0.1", port = 3000)
