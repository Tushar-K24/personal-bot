from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from ..settings.globals import DATABASE_CONFIG, DB_ECHO


class Base(DeclarativeBase):
    pass


print(DATABASE_CONFIG.url)  # for debugging
engine = create_async_engine(DATABASE_CONFIG.url, echo=DB_ECHO)
SessionMaker = async_sessionmaker(engine)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    db = SessionMaker()
    try:
        yield db
    finally:
        await db.close()
