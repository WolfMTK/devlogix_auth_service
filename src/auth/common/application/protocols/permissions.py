from abc import abstractmethod
from typing import Protocol


class BearerProvider(Protocol):
    @abstractmethod
    async def get_username(self) -> str:
        raise NotImplementedError
