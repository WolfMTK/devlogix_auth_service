from typing import Sequence

from sqlalchemy.ext.asyncio import async_sessionmaker

from models.tasks import Tasks
from .exceptions import InvalidNameTaskError
from .unit_of_work import UnitOfWork


class TaskService:
    async def add_task(self,
                       session_pool: async_sessionmaker,
                       user_id: str,
                       **kwargs) -> Tasks:
        uow = UnitOfWork(session_pool)
        async with uow:
            user = await uow.users.find_one(user_id=user_id)
            task = await uow.tasks.add_one(**(kwargs | {'user_id': user.id}))
            await uow.commit()
            return task

    async def get_task(self,
                       session_pool: async_sessionmaker,
                       user_id: str,
                       name: str) -> Tasks:
        uow = UnitOfWork(session_pool)
        async with uow:
            user = await uow.users.find_one(user_id=user_id)
            task = await uow.tasks.find_one(user_id=user.id, name=name)
            if not task:
                raise InvalidNameTaskError
            await uow.commit()
            return task

    async def get_tasks(
            self,
            session_pool: async_sessionmaker,
            user_id: str
    ) -> Sequence[Tasks] | None:
        uow = UnitOfWork(session_pool)
        async with uow:
            user = await uow.users.find_one(user_id=user_id)
            tasks = await uow.tasks.find_all(order_by='name', user_id=user.id)
            await uow.commit()
            return tasks

    async def delete_task(self,
                          session_pool: async_sessionmaker,
                          user_id: str,
                          name: str) -> None:
        uow = UnitOfWork(session_pool)
        async with uow:
            user = await uow.users.find_one(user_id=user_id)
            if not await uow.tasks.find_one(user_id=user.id, name=name):
                raise InvalidNameTaskError
            await uow.tasks.delete_one(user_id=user.id, name=name)
            await uow.commit()
