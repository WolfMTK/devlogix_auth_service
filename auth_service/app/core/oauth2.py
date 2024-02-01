from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from pydantic import ValidationError

from app.application.services import UserService, TokenService
from app.core.dependencies import UoWDep
from app.core.jwt import decode_token
from app.domain.schemas.tokens import TokenData
from app.domain.schemas.users import UserGet

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/jwt/token/')


async def get_current_user(uow: UoWDep,
                           token: str = Depends(oauth2_scheme)) -> UserGet:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'})
    try:
        if ((username := decode_token(token).get('sub')) is None or
                not (await TokenService().check_token(uow, token))):
            raise credentials_exception
        token_data = TokenData(username=username)
        return await UserService().get_user(uow, token_data.username)
    except (PyJWTError, AttributeError, ValidationError):
        raise credentials_exception


async def get_current_active_user(
        current_user: UserGet = Depends(get_current_user)
) -> UserGet:
    if current_user.is_active:
        return current_user
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail='Пользователь не активен!')
