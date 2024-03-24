from collections.abc import AsyncIterator
from contextlib import asynccontextmanager, AbstractAsyncContextManager

from fastapi import Depends

from auth.common.application.protocols.uow import UoW
from auth.user.adapters.stub_db import StubUserGateway
from auth.user.application.create_user import CreateUser
from auth.user.application.get_me import GetUserMe
from auth.user.domain.services.user import UserService
from auth.user.presentation.interactor_factory import UserInteractorFactory


class UserIOC(UserInteractorFactory):
    def __init__(
            self,
            uow: UoW = Depends(),
            gateway: StubUserGateway = Depends(),
    ):
        self.gateway = gateway
        self.uow = uow
        self.user_service = UserService()

    @asynccontextmanager
    async def create_user(self) -> AsyncIterator[CreateUser]:
        yield CreateUser(
            uow=self.uow,
            user_db_gateway=self.gateway,
            user_service=self.user_service,
        )

    @asynccontextmanager
    async def get_user_me(self) -> AbstractAsyncContextManager[GetUserMe]:
        yield GetUserMe(
            uow=self.uow,
            user_db_gateway=self.gateway,
            user_service=self.user_service
        )