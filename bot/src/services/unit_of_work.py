from abc import ABC, abstractmethod
from typing import Type

from sqlalchemy.ext.asyncio import async_sessionmaker

from repositories.users import UsersRepository
from repositories.tasks import TasksRepository


class AbstractUnitOfWork(ABC):
    users = Type[UsersRepository]
    tasks = Type[TasksRepository]

    @abstractmethod
    def __init__(self): ...

    @abstractmethod
    async def __aenter__(self): ...

    @abstractmethod
    async def __aexit__(self, *args): ...

    @abstractmethod
    async def commit(self): ...


class UnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_pool: async_sessionmaker) -> None:
        self.session_pool = session_pool

    async def __aenter__(self):
        self.session = self.session_pool()

        self.users = UsersRepository(self.session)
        self.tasks = TasksRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
