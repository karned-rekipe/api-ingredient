from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from project.dependencies.security import get_credentials
from project.config import *


class CustomMiddleware(BaseHTTPMiddleware):
    async def dispatch(
            self, request: Request, call_next: RequestResponseEndpoint
    ):
        if (
            request.url.path.startswith(f"/v{api_v}/{api}/docs") or
            request.url.path.startswith(f"/v{api_v}/{api}/openapi.json") or
            request.url.path.startswith(f"/v{api_v}/{api}/healthchecker")
        ):
            return await call_next(request)

        try:
            credentials = get_credentials(request.headers)
        except Exception as err:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "message": "You are not authorized to use this api",
                    "error message": f"Unexpected {err=}"
                }
            )

        response = await call_next(request)
        return response
