from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import PyJWTError

from auth.application.services import UserService
from auth.core.jwt import decode_token
from auth.domain.schemas import UserGet, TokenData
from auth.application.services.exceptions import EmptyUserException
from .dependencies import UoWDep

bearer_token = HTTPBearer(auto_error=False)


async def get_current_user(
        uow: UoWDep,
        auth: HTTPAuthorizationCredentials = Depends(bearer_token)
) -> UserGet:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Не удалось подтвердить данные!',
        headers={'WWW-Authenticate': 'Bearer'})
    token = auth.credentials
    try:
        if ((username := decode_token(token).get('sub')) is None):
            raise credentials_exception
        token_data = TokenData(username=username)

        return await UserService().get_user(uow, token_data.username)
    except (PyJWTError, AttributeError, EmptyUserException):
        raise credentials_exception


async def get_current_active_user(
        current_user: UserGet = Depends(get_current_user)
) -> UserGet:
    if current_user.is_active:
        return current_user
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail='Пользователь не активен!')
