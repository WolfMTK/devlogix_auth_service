from collections.abc import AsyncIterator

from fastapi import Depends
from redis.asyncio.client import AbstractRedis

from auth.token.adapters.database.redis import RedisClient


async def new_redis_connect(
        redis: AbstractRedis = Depends(AbstractRedis)
) -> AsyncIterator[RedisClient]:
    yield RedisClient(redis)
