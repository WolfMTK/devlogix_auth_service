from typing import Sequence

from sqlalchemy import delete, select

from models.tasks import Tasks
from .repository import SQLAlchemyRepository


class TasksRepository(SQLAlchemyRepository):
    model = Tasks

    async def delete_one(self, **kwargs) -> None:
        stmt = delete(self.model).filter_by(**kwargs)
        await self.session.execute(stmt)

    async def find_all(self,
                       order_by: str,
                       **kwargs) -> Sequence[Tasks] | None:
        stmt = select(self.model).filter_by(**kwargs).order_by(order_by)
        result = await self.session.execute(stmt)
        return result.scalars().all()
