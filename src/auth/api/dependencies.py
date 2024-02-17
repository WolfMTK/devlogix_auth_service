from typing import Annotated

from redis.asyncio.client import Pipeline
from fastapi import Depends

from auth.application.protocols.unit_of_work import (
    UnitOfWork,
    UoW,
)
from auth.infrastructure.db import async_session_maker
from auth.infrastructure.redis import create_connect


def connect_database() -> UnitOfWork:
    return UnitOfWork(async_session_maker)


UoWDep = Annotated[UoW, Depends(connect_database)]
RedisConnect = Annotated[Pipeline, Depends(create_connect)]
