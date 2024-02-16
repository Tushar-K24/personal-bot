from fastapi.responses import JSONResponse
from typing import Any


class AppException(Exception):
    def __init__(self, status_code: int, data: dict[str, Any]):
        self.status_code = status_code
        self.data = data


def success_response_builder(data: Any, status_code: int = 200) -> JSONResponse:
    return JSONResponse({"data": data, "error": None}, status_code=status_code)
