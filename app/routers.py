from fastapi import FastAPI

from app.core import auth
from app.services import user_data_builder, api_a, api_b


def load_routers(app: FastAPI) -> None:
    app.include_router(auth.router)
    app.include_router(api_a.router)
    app.include_router(api_b.router)
    app.include_router(user_data_builder.router)
