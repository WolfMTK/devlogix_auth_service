from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import PyJWTError
from redis.asyncio.client import AbstractRedis, Pipeline

from auth.application.exceptions import EmptyUserException
from auth.application.models import UserGet, TokenData
from auth.application.protocols.database import UoWDatabase
from auth.application.services import UserService
from auth.core.jwt import decode_token

bearer_token = HTTPBearer(auto_error=False)


async def get_current_user(
        redis: AbstractRedis = Depends(),
        uow: UoWDatabase = Depends(),
        auth: HTTPAuthorizationCredentials = Depends(bearer_token)
) -> UserGet:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Не удалось подтвердить данные.',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    redis: Pipeline = redis  # noqa
    try:
        token = auth.credentials
        if (username := decode_token(token).get('sub')) is None:
            raise credentials_exception
        token_data = TokenData(username=username)
        user = await UserService().get_user(uow, token_data.username)
        await redis.get(f'access-token::{user.id}')
        user_token = (await redis.execute())[0].decode('utf-8')
        if not (user_token == token):
            raise credentials_exception
        return user
    except (PyJWTError, AttributeError, EmptyUserException):
        raise credentials_exception


async def get_current_active_user(
        current_user: UserGet = Depends(get_current_user)
) -> UserGet:
    return await _get_user(current_user, 'is_active')


async def get_current_admin(
        current_user: UserGet = Depends(
            get_current_active_user
        )
):
    return await _get_user(current_user, 'is_admin')


async def _get_user(current_user: UserGet, value: str) -> UserGet:
    if getattr(current_user, value):
        return current_user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='Доступ запрещён.',
    )
