from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.routers import load_routers
from app.utils.db_connection import db


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
