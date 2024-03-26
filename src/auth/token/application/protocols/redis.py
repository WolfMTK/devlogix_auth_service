import datetime as dt
from abc import abstractmethod
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
