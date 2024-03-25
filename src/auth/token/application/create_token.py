import datetime as dt
import uuid
from dataclasses import dataclass

from auth.common.application.protocols.interactor import Interactor
from auth.common.application.protocols.jwt import TokenProvider
from auth.common.application.protocols.uow import UoW
from auth.core.config import TokenTime
from auth.token.adapters.stub_db import StubTokenGateway
from auth.token.domain.services.token import TokenService


@dataclass
class TokenResultDTO:
    accessToken: str
    expiresIn: int
    refreshToken: uuid.UUID
    tokenType: str


@dataclass
class UserDTO:
    password: str
    username: str | None = None
    email: str | None = None


class CreateToken(Interactor[UserDTO, TokenResultDTO]):
    def __init__(
            self,
            uow: UoW,
            token_db_gateway: StubTokenGateway,
            token_service: TokenService,
            jwt: TokenProvider
    ):
        self.uow = uow
        self.token_db_gateway = token_db_gateway
        self.token_service = token_service
        self.jwt = jwt

    async def __call__(self, token: UserDTO) -> TokenResultDTO:
        await self.token_service.check_username_and_email(
            token.username,
            token.email
        )
        await self.token_service.check_user(
            await self.token_db_gateway.check_user(
                username=token.username, email=token.email
            ),
            token.username,
            token.email
        )
        user = await self.token_db_gateway.get_user(
            username=token.username, email=token.email
        )
        access_token = self.jwt.create_token({'sub': token.username})
        refresh_token = await self.token_service.create_refresh_token(
            user.username
        )
        await self.token_db_gateway.create_token(user, refresh_token)
        access_time_token = dt.timedelta(
            minutes=int(TokenTime().time_access_token)
        )

        return TokenResultDTO(
            accessToken=access_token,
            expiresIn=int(access_time_token.total_seconds()),
            refreshToken=refresh_token,
            tokenType='Bearer'
        )
