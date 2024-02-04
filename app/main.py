from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from fastapi import FastAPI
from sqlalchemy.schema import MetaData

from app.core import auth
from app.routes import views

from app.database.connection import initDB

app: FastAPI = FastAPI()
db: MetaData = initDB(app)


# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(views.router)
