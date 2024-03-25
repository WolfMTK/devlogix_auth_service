import uuid
from abc import abstractmethod
from typing import Protocol

from auth.token.adapters.database.models import Token
from auth.user.adapters.database.models import User


class TokenCreated(Protocol):
    @abstractmethod
    async def create_token(self, user: User, token: uuid.UUID) -> Token:
        raise NotImplementedError
