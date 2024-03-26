from abc import ABC, abstractmethod
from contextlib import AbstractAsyncContextManager

from auth.token.application.create_token import CreateToken
from auth.token.application.delete_token import DeleteToken


class TokenInteractorFactory(ABC):
    @abstractmethod
    def create_token(self) -> AbstractAsyncContextManager[CreateToken]:
        raise NotImplementedError

    @abstractmethod
    def delete_token(self) -> AbstractAsyncContextManager[DeleteToken]:
        raise NotImplementedError
