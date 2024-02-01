from sqlalchemy.ext.asyncio import async_sessionmaker

from models.users import Users
from .unit_of_work import UnitOfWork


class UsersService:
    async def get_user(self,
                       session_pool: async_sessionmaker,
                       **kwargs) -> Users | None:
        uow = UnitOfWork(session_pool)
        async with uow:
            user = await uow.users.find_one(**kwargs)
            await uow.commit()
            return user

    async def add_user(self,
                       session_pool: async_sessionmaker,
                       **kwargs) -> Users:
        uow = UnitOfWork(session_pool)
        async with uow:
            user = await uow.users.add_one(**kwargs)
            await uow.commit()
            return user
