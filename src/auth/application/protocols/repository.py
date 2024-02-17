from abc import ABC, abstractmethod
from typing import TypeVar, Sequence, Any

from sqlalchemy import insert, select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from auth.infrastructure.db import Base

ModelType = TypeVar('ModelType', bound=Base)


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, *args, **kwargs):
        ...

    @abstractmethod
    async def update_one(self, *args, **kwargs):
        ...

    @abstractmethod
    async def find_one(self, *args, **kwargs):
        ...

    @abstractmethod
    async def find_all(self, *args, **kwargs):
        ...

    @abstractmethod
    async def delete_one(self, *args, **kwargs):
        ...


class SQLAlchemyRepository(AbstractRepository):
    model: ModelType | None = None

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_one(
            self,
            **kwargs: dict[str, Any]
    ) -> ModelType:
        """Добавление записи в БД."""
        stmt = insert(self.model).values(**kwargs).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def update_one(self, id: int, **kwargs) -> ModelType:
        """Обновление записи в БД."""
        stmt = update(self.model).filter(
            self.model.id == id
        ).values(**kwargs).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def find_one(self, **filter_by: dict[str, Any]) -> ModelType | None:
        """Поиск записи в БД."""
        stmt = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def find_all(
            self, order_by: str | None = None
    ) -> Sequence[ModelType]:
        """Поиск записей в БД."""
        stmt = select(self.model).order_by(order_by)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def delete_one(self, **filter_by: dict[str, Any]) -> None:
        """Удаление записи в БД."""
        stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(stmt)
