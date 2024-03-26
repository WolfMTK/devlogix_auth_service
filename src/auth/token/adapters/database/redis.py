import datetime as dt
from typing import Awaitable

from redis.asyncio.client import AbstractRedis, Redis

from auth.token.application.protocols.redis import RedisUoW, RedisT


class RedisClient(RedisUoW):
    def __init__(self, redis: AbstractRedis):
        self.redis: Redis = redis  # noqa

    async def set(
            self,
            name: RedisT,
            value: int | float | RedisT,
            ex: None | int | dt.timedelta
    ) -> None:
        await self.redis.set(name, value, ex=ex)

    async def get(self, name: RedisT) -> Awaitable:
        return await self.redis.get(name)
