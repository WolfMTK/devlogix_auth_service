from auth.common.application.protocols.interactor import Interactor
from auth.common.application.protocols.uow import UoW
from auth.user.adapters.database.models import User
from auth.user.adapters.stub_db import StubUserGateway
from auth.user.domain.models.user import UserDTO, UserResultDTO
from auth.user.domain.services.user import UserService


class CreateUser(Interactor[UserDTO, UserResultDTO]):
    def __init__(
            self,
            uow: UoW,
            user_db_gateway: StubUserGateway,
            user_service: UserService,
    ):
        self.uow = uow
        self.user_db_gateway = user_db_gateway
        self.user_service = user_service

    async def __call__(self, user: UserDTO) -> UserResultDTO:
        self.user_service.check_email_exists(
            await self.user_db_gateway.check_user(email=user.email)
        )
        self.user_service.check_username_exists(
            await self.user_db_gateway.check_user(username=user.username)
        )

        model = await self.user_db_gateway.get_user(
            username=user.username,
            email=user.email
        )

        if model is not None:
            self.user_service.set_is_active_user(model)
        else:
            model = User(
                email=user.email,
                username=user.username,
                password=user.password
            )

        await self.user_db_gateway.create_user(model)

        await self.uow.commit()
        return UserResultDTO(
            id=model.id,
            email=model.email,
            username=model.username
        )
