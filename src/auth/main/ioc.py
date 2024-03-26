from collections.abc import AsyncIterator
from contextlib import asynccontextmanager, AbstractAsyncContextManager

from fastapi import Depends

from auth.common.application.protocols.jwt import TokenProvider
from auth.common.application.protocols.uow import UoW
from auth.token.adapters.stub_db import StubTokenGateway
from auth.token.application.create_token import CreateToken
from auth.token.domain.services.token import TokenService
from auth.token.presentation.interactor_factory import TokenInteractorFactory
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
    ) -> None:
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
    async def get_user_me(self) -> AsyncIterator[GetUserMe]:
        yield GetUserMe(
            uow=self.uow,
            user_db_gateway=self.gateway,
            user_service=self.user_service
        )


class TokeIOC(TokenInteractorFactory):
    def __init__(
            self,
            uow: UoW = Depends(),
            gateway: StubTokenGateway = Depends(),
            jwt: TokenProvider = Depends()
    ) -> None:
        self.uow = uow
        self.gateway = gateway
        self.token_service = TokenService()
        self.jwt = jwt

    @asynccontextmanager
    async def create_token(self) -> AsyncIterator[CreateToken]:
        yield CreateToken(
            uow=self.uow,
            token_db_gateway=self.gateway,
            token_service=self.token_service,
            jwt=self.jwt
        )
