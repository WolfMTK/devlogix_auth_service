from abc import abstractmethod, ABC
from contextlib import AbstractAsyncContextManager

from auth.user.application.create_user import CreateUser
from auth.user.application.read_user_me import GetUserMe
from auth.user.application.update_user_me import UpdateUserMe


class UserInteractorFactory(ABC):
    @abstractmethod
    def create_user(self) -> AbstractAsyncContextManager[CreateUser]:
        raise NotImplementedError

    @abstractmethod
    def get_user_me(self) -> AbstractAsyncContextManager[GetUserMe]:
        raise NotImplementedError

    @abstractmethod
    def update_user_me(self) -> AbstractAsyncContextManager[UpdateUserMe]:
        raise NotImplementedError
