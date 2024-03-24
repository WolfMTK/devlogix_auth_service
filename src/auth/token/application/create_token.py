from dataclasses import dataclass

from auth.common.application.protocols.interactor import Interactor
from auth.common.application.protocols.uow import UoW
from auth.token.adapters.stub_db import StubTokenGateway
from auth.token.domain.services.token import TokenService


@dataclass
class TokenResultDTO:
    name: str


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
            token_service: TokenService
    ):
        self.uow = uow
        self.token_db_gateway = token_db_gateway
        self.token_service = token_service

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
        return TokenResultDTO(name='test')
