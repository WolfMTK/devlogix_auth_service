from auth.common.application.protocols.interactor import Interactor
from auth.common.application.protocols.uow import UoW
from auth.user.adapters.stub_db import StubUserGateway
from auth.user.domain.models.user import UserMeDTO, UserResultDTO
from auth.user.domain.services.user import UserService


class GetUserMe(Interactor[UserMeDTO, UserResultDTO]):
    def __init__(
            self,
            uow: UoW,
            user_db_gateway: StubUserGateway,
            user_service: UserService
    ) -> None:
        self.uow = uow
        self.user_db_gateway = user_db_gateway
        self.user_service = user_service

    async def __call__(self, user: UserMeDTO) -> UserResultDTO:
        model = await self.user_db_gateway.get_user(username=user.username)
        user = self.user_service.get_user_me(model)
        self.user_service.check_is_active(user)
        return UserResultDTO(
            id=user.id,
            username=user.username,
            email=user.email
        )
