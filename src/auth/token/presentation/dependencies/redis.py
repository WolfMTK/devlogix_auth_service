from fastapi import Depends

from auth.token.adapters.database.redis import RedisClient
from collections.abc import AsyncIterator

from redis.asyncio.client import AbstractRedis


async def new_redis_connect(
        redis: AbstractRedis = Depends(AbstractRedis)
) -> AsyncIterator[RedisClient]:
    yield RedisClient(redis)
