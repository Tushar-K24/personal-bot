from typing import Optional

from fastapi import FastAPI

# from gino.ext.starlette import Gino
from gino_starlette import Gino

from ..settings.globals import DATABASE_CONFIG, DB_ECHO


def initialize_db(app: Optional[FastAPI] = None) -> Gino:
    db: Gino = Gino(dsn=DATABASE_CONFIG.url, echo=DB_ECHO)
    if app:
        db.init_app(app)
    return db


db = initialize_db()
