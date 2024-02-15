from fastapi import Request, Response
from fastapi.responses import JSONResponse
from typing import Any
from ..main import app


class AppException(Exception):
    def __init__(self, status_code: int, data: dict[str, Any]):
        self.status_code = status_code
        self.data = data


@app.exception_handler(AppException)
async def app_error_handler(request: Request, exc: AppException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code, content={"data": None, "error": exc.data}
    )


def success_response_builder(
    response: Response, data: Any, status_code: int = 200
) -> dict:
    response.status_code = status_code
    return {"data": data, "error": None}
