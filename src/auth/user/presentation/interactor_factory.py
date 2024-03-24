from abc import abstractmethod, ABC
from contextlib import AbstractAsyncContextManager

from auth.user.application.create_user import CreateUser
from auth.user.application.get_me import GetUserMe


class UserInteractorFactory(ABC):
    @abstractmethod
    def create_user(self) -> AbstractAsyncContextManager[CreateUser]:
        raise NotImplementedError

    @abstractmethod
    def get_user_me(self) -> AbstractAsyncContextManager[GetUserMe]:
        raise NotImplementedError
