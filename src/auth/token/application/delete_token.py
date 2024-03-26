from auth.common.application.protocols.interactor import Interactor
from auth.common.application.protocols.uow import UoW
from auth.token.adapters.stub_db import StubTokenGateway
from auth.token.application.protocols.redis import RedisUoW
from auth.user.domain.models.user_id import UserID


class DeleteToken(Interactor[UserID, None]):
    def __init__(
            self,
            uow: UoW,
            token_db_gateway: StubTokenGateway,
            redis: RedisUoW
    ):
        self.uow = uow
        self.token_db_gateway = token_db_gateway
        self.redis = redis

    async def __call__(self, user_id: UserID) -> None:
        await self.token_db_gateway.delete_token(user_id)
        await self.redis.delete(f'access-token::{user_id}')
        await self.uow.commit()
