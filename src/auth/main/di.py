from collections.abc import AsyncIterator
from functools import partial
from typing import TypeVar, Callable

from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

from auth.common.adapters.security.jwt import JWTProvider
from auth.common.adapters.security.password import PasswordCryptoProvider
from auth.common.application.protocols.jwt import TokenProvider
from auth.common.application.protocols.password import PasswordProvider
from auth.common.application.protocols.uow import UoW
from auth.common.presentation.dependencies.depends_stub import Stub
from auth.core.config import load_database_config, load_jwt_config

DependencyT = TypeVar("DependencyT")


def singleton(value: DependencyT) -> Callable[[], DependencyT]:
    def singleton_factory() -> DependencyT:
        return value

    return singleton_factory


def create_async_session_maker():
    engine = create_async_engine(load_database_config().db_uri)
    return async_sessionmaker(engine, expire_on_commit=False)


def new_uow(
        session: AsyncSession = Depends(Stub(AsyncSession))
) -> AsyncSession:
    return session


async def create_async_session(
        session_maker: async_sessionmaker
) -> AsyncIterator[AsyncSession]:
    async with session_maker() as session:
        yield session


def init_dependencies(app: FastAPI):
    session_maker = create_async_session_maker()
    jwt_config = load_jwt_config()
    jwt = JWTProvider(
        secret_token=jwt_config.secret_token,
        algorithm=jwt_config.algorithm
    )
    app.dependency_overrides.update(
        {
            AsyncSession: partial(create_async_session, session_maker),
            UoW: new_uow,
            PasswordProvider: PasswordCryptoProvider,
            TokenProvider: lambda: jwt,
        }
    )
