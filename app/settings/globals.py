from pathlib import Path
from typing import Optional

from sqlalchemy.engine.url import URL
from starlette.config import Config
from starlette.datastructures import Secret

from ..models.pydantic.database import DatabaseURL

p: Path = Path(__file__).parents[2] / ".env"
config: Config = Config(p if p.exists() else None)

DATABASE: str = config("DATABASE", cast=str)
DB_USER: Optional[str] = config("DB_USER", cast=str, default=None)
DB_PASSWORD: Optional[Secret] = config("DB_PASSWORD", cast=Secret, default=None)
DB_HOST: str = config("DB_HOST", cast=str, default="localhost")
DB_PORT: int = config("DB_PORT", cast=int, default=5432)
DB_ECHO: bool = config("DB_ECHO", cast=bool, default=True)

DATABASE_CONFIG: DatabaseURL = DatabaseURL(
    drivername="postgresql+asyncpg",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DATABASE,
)

# A hack as field validator for url is not working, need fixing
DATABASE_CONFIG.url = URL(
    drivername="postgresql+asyncpg",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DATABASE,
    query={}
)



REDIS_IP: str = config("REDIS_IP", cast=str, default="127.0.0.1")
REDIS_PORT: int = config("REDIS_PORT", cast=int, default=6379)

SERP_API_KEY: str = config("SERP_API_KEY", cast=str, default="")
