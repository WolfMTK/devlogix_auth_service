from auth.common.application.protocols.interactor import Interactor
from auth.user.adapters.database.models import User
from auth.user.domain.models.user import UserResultDTO


class GetUserMe(Interactor[User, UserResultDTO]):
    async def __call__(self, user: User) -> UserResultDTO:
        return UserResultDTO(
            id=user.id,
            username=user.username,
            email=user.email
        )
