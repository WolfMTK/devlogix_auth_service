from abc import ABC, abstractmethod
from typing import TypeVar

from auth.domain.models import Base

ModelType = TypeVar('ModelType', bound=Base)


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, *args, **kwargs):
        ...

    @abstractmethod
    async def update_one(self, *args, **kwargs):
        ...

    @abstractmethod
    async def find_one(self, *args, **kwargs):
        ...

    @abstractmethod
    async def find_all(self, *args, **kwargs):
        ...

    @abstractmethod
    async def delete_one(self, *args, **kwargs):
        ...
