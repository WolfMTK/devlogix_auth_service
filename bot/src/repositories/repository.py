from abc import ABC, abstractmethod
from typing import TypeVar

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db import Base

ModelType = TypeVar('ModelType', bound=Base)


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self): ...

    @abstractmethod
    async def find_one(self): ...


class SQLAlchemyRepository(AbstractRepository):
    model: ModelType | None = None

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_one(self, **kwargs) -> ModelType:
        stmt = insert(self.model).values(**kwargs).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def find_one(self, **kwargs) -> ModelType | None:
        stmt = select(self.model).filter_by(**kwargs)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
