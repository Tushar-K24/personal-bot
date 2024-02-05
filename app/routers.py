from app.core import auth
from app.routes import views
from fastapi import FastAPI


def load_routers(app: FastAPI) -> None:
    app.include_router(auth.router)
    app.include_router(views.router)
