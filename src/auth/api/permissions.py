from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import PyJWTError

from auth.application.protocols.unit_of_work import UoW
from auth.application.services import UserService
from auth.application.services.exceptions import EmptyUserException
from auth.core.jwt import decode_token
from auth.domain.schemas import UserGet, TokenData
from auth.api.dependencies import RedisConnect

bearer_token = HTTPBearer(auto_error=False)


async def get_current_user(
        redis: RedisConnect,
        uow: UoW = Depends(),
        auth: HTTPAuthorizationCredentials = Depends(bearer_token)
) -> UserGet:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Не удалось подтвердить данные.',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    try:
        token = auth.credentials
        if (username := decode_token(token).get('sub')) is None:
            raise credentials_exception
        token_data = TokenData(username=username)
        user = await UserService().get_user(uow, token_data.username)
        await redis.get(user.id)
        user_token = (await redis.execute())[0].decode('utf-8')
        if not (user_token == token):
            raise credentials_exception
        return user
    except (PyJWTError, AttributeError, EmptyUserException):
        raise credentials_exception


async def get_current_active_user(
        current_user: UserGet = Depends(get_current_user)
) -> UserGet:
    if current_user.is_active:
        return current_user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='Доступ запрещён.',
    )
