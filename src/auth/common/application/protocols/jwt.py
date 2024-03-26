from abc import abstractmethod
from typing import Protocol, Any


class TokenProvider(Protocol):
    @abstractmethod
    def create_token(self, data: dict[str, Any]) -> str:
        raise NotImplementedError

    @abstractmethod
    def decode_token(self, token: str) -> dict[str, Any]:
        raise NotImplementedError
