from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from fastapi import FastAPI

from app.utils.db_connection import db
from app.routers import load_routers


def get_app() -> FastAPI:
    app: FastAPI = FastAPI()
    db.init_app(app)
    # Set all CORS enabled origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    load_routers(app)
    return app
