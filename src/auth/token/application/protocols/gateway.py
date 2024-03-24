from abc import abstractmethod
from typing import Protocol

from auth.token.adapters.database.models import Token


class TokenCreated(Protocol):
    @abstractmethod
    async def create_token(self, token: Token) -> Token:
        raise NotImplementedError
