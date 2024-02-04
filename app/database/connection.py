from gino.ext.starlette import Gino
from fastapi import FastAPI
from sqlalchemy.schema import MetaData

from ..settings.globals import DATABASE_CONFIG, DB_ECHO


def initDB(app: FastAPI) -> MetaData:
    return Gino(app, dsn=DATABASE_CONFIG.url, echo=DB_ECHO)
