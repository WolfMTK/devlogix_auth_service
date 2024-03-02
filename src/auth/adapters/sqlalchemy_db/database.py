from sqlalchemy.ext.asyncio import async_sessionmaker

from auth.adapters.sqlalchemy_db.repositories import (
    UserRepository,
    TokenRepository,
)
from auth.application.protocols.database import UoWDatabase


class Session(UoWDatabase):
    def __init__(self, session_factory: async_sessionmaker) -> None:
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.users = UserRepository(self.session)
        self.tokens = TokenRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
