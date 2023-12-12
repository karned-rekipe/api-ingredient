from fastapi import Depends
from fastapi.security import HTTPBearer
from pebbleauthclient import auth_from_http_headers

security = HTTPBearer()


def get_credentials(token: dict = Depends(security)):
    auth_token = auth_from_http_headers(token)
    return auth_token
