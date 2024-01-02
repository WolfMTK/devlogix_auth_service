from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Body, Depends, Response

from fastapi.security import OAuth2PasswordRequestForm

from src.application.services import UserService, TokenService
from src.core import exceptions
from src.core.dependencies import UoWDep
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
        uow: UoWDep,
        user: UserCreate = Body(..., example=BODY_USER_CREATE_EXAMPLE)
) -> User:
    """
    Регистрация пользователя.

     - **username** - юзернейм

     - **email** - почта

     - **password** - пароль (длина пароля больше или равна 8 символам)

     **username**, **email**, **password** являются обязательными.
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
async def login(uow: UoWDep,
                user: UserLogin = Body(...,
                                       example=BODY_USER_CREATE_EXAMPLE)):
    """
    Аутентификация пользователя.

    **username** - юзернейм

    **email** - почта

    **password** - пароль

    **username/email** и **password** являются обязательными.
    """
    try:
        return await TokenService().get_token(uow, user)
    except exceptions.HTTPError401 as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'{error}',
            headers={"WWW-Authenticate": "Bearer"},
        )


# TODO: временная ручка, будет скрыта в будущем
@router.post("/token/", response_model=TokenGet)
async def login_for_access_token(
        uow: UoWDep,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = UserLogin(username=form_data.username, password=form_data.password)
    try:
        return await TokenService().get_token(uow, user)
    except exceptions.HTTPError401 as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'{error}',
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post('/logout/', status_code=status.HTTP_204_NO_CONTENT)
async def logout(
        current_user: Annotated[
            UserGet, Depends(get_current_active_user)
        ],
        uow: UoWDep
) -> Response:
    """Разлогирование пользователя."""
    await TokenService().delete_token(uow, current_user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get('/token-clear-users/', include_in_schema=False)
async def clear_tokens_in_database(uow: UoWDep) -> None:
    """Очистка токенов с истекшим сроком действия."""
    await TokenService().clear_tokens(uow)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                        detail='Method Not Allowed')
