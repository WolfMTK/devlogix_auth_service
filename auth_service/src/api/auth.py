from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Body, Depends, Response

from src.application.services import UserService, TokenService
from src.core import exceptions
from src.core.dependencies import UOWDep
from src.core.oauth2 import get_current_active_user
from src.core.swagger import (
    BODY_USER_CREATE_EXAMPLE,
    RESPONSE_USER_CREATE_EXAMPLE,
)
from src.domain.models.users import User
from src.domain.schemas.tokens import TokenGet
from src.domain.schemas.users import UserCreate, UserGet, UserLogin

router = APIRouter(prefix='/auth/jwt', tags=['auth'])


@router.post(
    '/register/',
    response_model=UserGet,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
    responses=RESPONSE_USER_CREATE_EXAMPLE
)
async def register_user(
        uow: UOWDep,
        user: UserCreate = Body(..., example=BODY_USER_CREATE_EXAMPLE)
) -> User:
    """
    Регистрация пользователя.

     - **username** - юзернейм
     - **email** - почта
     - **password** - пароль (длина пароля больше или равна 8 символам)
    """
    try:
        return await UserService().register_user(uow, user)
    except  exceptions.HTTPError400 as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


@router.post('/login/',
             response_model=TokenGet)
async def login(uow: UOWDep,
                user: UserLogin):
    """
    Аутентификация пользователя.

    **username** - юзернейм
    **email** - почта
    **password** - пароль
    """
    try:
        return await TokenService().get_token(uow, user)
    except exceptions.HTTPError401 as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'{error}',
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post('/logout/')
async def logout(
        uow: UOWDep,
        current_user: Annotated[
            UserGet, Depends(get_current_active_user)
        ]) -> Response:
    """Разлогирование пользователя."""
    await TokenService().delete_token(uow, current_user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get('/token-clear-users/', include_in_schema=False)
async def clear_tokens_in_database(uow: UOWDep) -> None:
    """Очистка токенов с истекшим сроком действия."""
    await TokenService().clear_tokens(uow)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                        detail='Method Not Allowed')
