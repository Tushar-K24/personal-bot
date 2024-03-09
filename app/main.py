from fastapi import Request
from fastapi.responses import JSONResponse

from app.routers import load_routers
from app.utils.app import get_app
from app.core.exception_handler import AppException

app = get_app()
load_routers(app)


@app.exception_handler(AppException)
async def app_error_handler(request: Request, exc: AppException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code, content={"data": None, "error": exc.data}
    )


@app.get("/")
async def index() -> dict[str, str]:
    return {
        "info": "This is the index page of fastapi-nano. "
        "You probably want to go to 'http://<hostname:port>/docs'.",
    }
