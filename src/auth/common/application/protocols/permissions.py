from abc import abstractmethod
from typing import Protocol

from auth.user.adapters.database.models import User


class BearerProvider(Protocol):
    @abstractmethod
    async def get_username(self) -> User:
        raise NotImplementedError
