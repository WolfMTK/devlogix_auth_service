from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import PyJWTError

from auth.common.application.protocols.jwt import TokenProvider
from auth.common.application.protocols.permissions import BearerProvider
from auth.common.presentation.dependencies.depends_stub import Stub

bearer_token = HTTPBearer(auto_error=False)


class PermissionBearerProvider(BearerProvider):
    def __init__(
            self,
            bearer: HTTPAuthorizationCredentials = Depends(bearer_token),
            jwt: TokenProvider = Depends(Stub(TokenProvider)),
    ):
        self.bearer = bearer
        self.jwt = jwt

    async def get_username(self) -> str:
        try:
            token = await self._get_credentials()
            if (username := self.jwt.decode_token(token).get('sub')) is None:
                return self._is_unauthorized()
            return username
        except PyJWTError:
            return self._is_unauthorized()

    def _is_unauthorized(self):
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
