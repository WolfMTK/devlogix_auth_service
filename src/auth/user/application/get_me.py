from dataclasses import dataclass

from auth.common.application.protocols.interactor import Interactor
from auth.common.application.protocols.uow import UoW
from auth.user.adapters.stub_db import StubUserGateway
from auth.user.domain.models.user import UserResult
from auth.user.domain.services.user import UserService


@dataclass
class UserMeDTO:
    username: str


class GetUserMe(Interactor[UserMeDTO, UserResult]):
    def __init__(
            self,
            uow: UoW,
            user_db_gateway: StubUserGateway,
            user_service: UserService
    ):
        self.uow = uow
        self.user_db_gateway = user_db_gateway
        self.user_service = user_service

    async def __call__(self, user: UserMeDTO) -> UserResult:
        model = await self.user_db_gateway.get_user(username=user.username)
        user = self.user_service.get_user_me(model)
        self.user_service.check_is_active(user)
        return UserResult(
            id=user.id,
            username=user.username,
            email=user.email
        )
