import datetime as dt
from abc import abstractmethod
from collections.abc import Awaitable
from typing import Protocol

RedisT = str | bytes | memoryview


class RedisUoW(Protocol):
    @abstractmethod
    async def set(
            self,
            name: RedisT,
            value: int | float | RedisT,
            ex: None | int | dt.timedelta
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get(self, name: RedisT) -> Awaitable:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, name: RedisT) -> None:
        raise NotImplementedError
