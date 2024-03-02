from functools import partial

import redis.asyncio as aioredis
from fastapi import FastAPI
from redis.client import AbstractRedis
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from auth.adapters.sqlalchemy_db.database import Session
from auth.application.protocols.database import UoWDatabase
from auth.core import Settings


def create_redis_connect():
    return aioredis.from_url(Settings.redis).pipeline()


def create_async_session_maker():
    engine = create_async_engine(
        url=Settings.db_url,
        echo=False
    )
    return async_sessionmaker(engine, expire_on_commit=False)


def init_dependencies(app: FastAPI) -> None:
    app.dependency_overrides[UoWDatabase] = partial(
        Session,
        create_async_session_maker()
    )
    app.dependency_overrides[AbstractRedis] = create_redis_connect
