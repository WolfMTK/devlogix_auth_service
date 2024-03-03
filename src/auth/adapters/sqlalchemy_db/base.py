import uuid
from collections.abc import Sequence
from typing import Any

from sqlalchemy import insert, update, select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from auth.application.protocols.repository import (
    AbstractRepository,
    ModelType,
)


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
        return result.unique().scalar_one()

    async def update_one(self, id: int | uuid.UUID, **kwargs) -> ModelType:
        """Обновление записи в БД."""
        stmt = update(self.model).filter(
            self.model.id == id
        ).values(**kwargs).returning(self.model)
        result = await self.session.execute(stmt)
        return result.unique().scalar_one()

    async def find_one(self, **filter_by: dict[str, Any]) -> ModelType | None:
        """Поиск записи в БД."""
        stmt = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(stmt)
        return result.unique().scalar_one_or_none()

    async def find_all(
            self, order_by: str | None = None
    ) -> Sequence[ModelType]:
        """Поиск записей в БД."""
        stmt = select(self.model).order_by(order_by)
        result = await self.session.execute(stmt)
        return result.unique().scalars().all()

    async def delete_one(self, **filter_by: dict[str, Any]) -> None:
        """Удаление записи в БД."""
        stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(stmt)
