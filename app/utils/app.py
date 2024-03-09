from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from app.core.middleware import log_request_middleware  # , SQLAlchemyMiddleware
from app.core.exception_handler import (
    request_validation_exception_handler,
    http_exception_handler,
    unhandled_exception_handler,
)


def get_app() -> FastAPI:
    app: FastAPI = FastAPI()
    # Set all CORS enabled origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # app.add_middleware(SQLAlchemyMiddleware)

    app.middleware("http")(log_request_middleware)
    app.add_exception_handler(
        RequestValidationError, request_validation_exception_handler
    )
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)

    return app
