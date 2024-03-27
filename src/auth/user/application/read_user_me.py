from auth.common.application.protocols.interactor import Interactor
from auth.user.adapters.database.models import User
from auth.user.domain.models.user import UserResult


class GetUserMe(Interactor[User, UserResult]):
    async def __call__(self, user: User) -> UserResult:
        return UserResult(
            id=user.id,
            username=user.username,
            email=user.email
        )
