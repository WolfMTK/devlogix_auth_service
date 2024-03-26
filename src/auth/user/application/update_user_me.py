from dataclasses import dataclass

from auth.common.application.protocols.interactor import Interactor
from auth.common.application.protocols.uow import UoW
from auth.user.adapters.stub_db import StubUserGateway
from auth.user.domain.models.user import UserResult, UserUpdate
from auth.user.domain.models.user_id import UserID
from auth.user.domain.services.user import UserService


@dataclass
class UserUpdateDTO:
    id: UserID
    value: UserUpdate


class UpdateUserMe(Interactor[UserUpdateDTO, UserResult]):
    def __init__(
            self,
            uow: UoW,
            user_db_gateway: StubUserGateway,
            user_service: UserService,
    ) -> None:
        self.uow = uow
        self.user_db_gateway = user_db_gateway
        self.user_service = user_service

    async def __call__(self, user: UserUpdateDTO) -> UserResult:
        self.user_service.check_username_exists(
            await self.user_db_gateway.check_user_username(
                user_id=user.id,
                username=user.value.username
            )
        )
        self.user_service.check_email_exists(
            await self.user_db_gateway.check_user_email(
                user_id=user.id,
                email=user.value.email
            )
        )
        self.user_service.check_email(user.value.email)
        user = await self.user_db_gateway.update_user(
            user_id=user.id,
            **self.user_service.update_user(user.value)
        )
        await self.uow.commit()
        return UserResult(
            id=user.id,
            username=user.username,
            email=user.email
        )
