import uuid
from abc import abstractmethod

from auth.user.application.protocols.gateway import (
    UserCreated,
    UserCheck,
    UserReading,
    UserUpdate,
)


class StubUserGateway(UserCreated, UserCheck, UserReading, UserUpdate):
    @abstractmethod
    async def check_user_username(
            self,
            user_id: uuid.UUID,
            username: str
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def check_user_email(self, user_id: uuid.UUID, email: str) -> bool:
        raise NotImplementedError
)
