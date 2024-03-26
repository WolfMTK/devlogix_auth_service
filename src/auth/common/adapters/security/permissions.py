from typing import Never

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import PyJWTError

from auth.common.application.protocols.jwt import TokenProvider
from auth.common.application.protocols.permissions import BearerProvider
from auth.common.presentation.dependencies.depends_stub import Stub
from auth.token.application.protocols.redis import RedisUoW
from auth.user.adapters.database.models import User
from auth.user.adapters.stub_db import StubUserGateway

bearer_token = HTTPBearer(auto_error=False)


class PermissionBearerProvider(BearerProvider):
    def __init__(
            self,
            bearer: HTTPAuthorizationCredentials = Depends(bearer_token),
            jwt: TokenProvider = Depends(Stub(TokenProvider)),
            redis: RedisUoW = Depends(),
            gateway: StubUserGateway = Depends()
    ) -> None:
        self.bearer = bearer
        self.jwt = jwt
        self.redis = redis
        self.gateway = gateway

    async def get_username(self) -> User:
        try:
            token = await self._get_credentials()
            if (username := self.jwt.decode_token(token).get('sub')) is None:
                return self._is_unauthorized()
            user = await self.gateway.get_user(username=username)
            await self._check_token(f'access-token::{user.id}')
            return user
        except PyJWTError:
            return self._is_unauthorized()

    async def _check_token(self, token: str) -> None:
        if await self.redis.get(token) is None:
            return self._is_unauthorized()

    def _is_unauthorized(self) -> Never:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid authentication credentials.',
            headers={'WWW-Authenticate': 'Bearer'}
        )

    async def _get_credentials(self) -> str:
        try:
            return self.bearer.credentials
        except AttributeError:
            return self._is_unauthorized()
