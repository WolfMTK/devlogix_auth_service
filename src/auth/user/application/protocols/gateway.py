import uuid
from abc import abstractmethod
from typing import Protocol, Any

from auth.user.adapters.database.models import User


class UserCreated(Protocol):
    @abstractmethod
    async def create_user(self, user: User) -> User:
        raise NotImplementedError


class UserCheck(Protocol):
    @abstractmethod
    async def check_user(self, *args, **filter_by: Any) -> bool:
        raise NotImplementedError


class UserReading(Protocol):
    @abstractmethod
    async def get_user(self, **filter_by: Any) -> User:
        raise NotImplementedError


class UserUpdate(Protocol):
    @abstractmethod
    async def update_user(self, user_id: uuid.UUID, **filter_by: Any) -> User:
        raise NotImplementedError
