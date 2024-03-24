from abc import ABC, abstractmethod
from contextlib import AbstractAsyncContextManager

from auth.token.application.create_token import CreateToken


class TokenInteractorFactory(ABC):
    @abstractmethod
    def create_token(self) -> AbstractAsyncContextManager[CreateToken]:
        raise NotImplementedError
