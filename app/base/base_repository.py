from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Union

from sqlalchemy import select, and_

from sqlalchemy.ext.asyncio import AsyncSession

Entity = TypeVar("Entity")


class BaseRepository(ABC, Generic[Entity]):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def getEntity(self) -> Entity:
        pass

    async def create(self, data: Union[Entity, List[Entity]], session: AsyncSession):
        entity = self.getEntity()
        if not isinstance(data, List):
            data = [entity(**data)]
        else:
            data = [entity(**d) for d in data]
        try:
            session.add_all(data)
            await session.commit()
            for d in data:
                await session.refresh(d)
            return data
        except Exception as e:
            await session.rollback()
            raise e

    async def find(self, filters: dict, session: AsyncSession):
        entity = self.getEntity()
        result = await session.scalars(
            select(entity).where(
                and_(
                    *[getattr(entity, attr) == value for attr, value in filters.items()]
                )
            )
        )
        return result.all()
