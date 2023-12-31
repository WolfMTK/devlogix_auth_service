from abc import ABC, abstractmethod
from typing import Type

from sqlalchemy.ext.asyncio import async_sessionmaker

from src.application.repositories.tokens import (
    AccessTokenRepository,
    RefreshTokenRepository,
)
from src.application.repositories.users import UserRepository


class UoW(ABC):
    users = Type[UserRepository]
    access_token = Type[AccessTokenRepository]
    refresh_token = Type[RefreshTokenRepository]

    @abstractmethod
    async def __aenter__(self): ...

    @abstractmethod
    async def __aexit__(self, *args): ...

    @abstractmethod
    async def commit(self): ...

    @abstractmethod
    async def rollback(self): ...


class UnitOfWork:
    def __init__(self, session_factory: async_sessionmaker) -> None:
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.users = UserRepository(self.session)
        self.access_token = AccessTokenRepository(self.session)
        self.refresh_token = RefreshTokenRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
