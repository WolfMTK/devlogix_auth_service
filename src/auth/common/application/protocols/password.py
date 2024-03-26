from typing import Protocol
from abc import abstractmethod


class PasswordProvider(Protocol):
    @abstractmethod
    def verify_password(
            self, secret: str | bytes,
            hash: str | bytes | None = None
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_password_hash(self, secret: str | bytes) -> str:
        raise NotImplementedError
