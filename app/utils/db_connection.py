from contextlib import asynccontextmanager

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
)

from ..settings.globals import DATABASE_CONFIG, DB_ECHO

from app.models.orm import Base


print(DATABASE_CONFIG.url)  # for debugging
engine = create_async_engine(DATABASE_CONFIG.url, echo=DB_ECHO)
SessionMaker = async_sessionmaker(engine)


@asynccontextmanager
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session = SessionMaker(autocommit=False, autoflush=False, bind=engine)

    try:
        yield session
    finally:
        await session.close()
