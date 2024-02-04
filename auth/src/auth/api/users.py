from typing import Annotated

from fastapi import APIRouter, status, Body, HTTPException, Depends, Response

from .auth import get_current_active_user
from auth.api.dependencies import UoWDep
from auth.api.swagger import (RESPONSE_USER_GET_EXAMPLE,
                              BODY_USER_CREATE_EXAMPLE)
from auth.application.services import exceptions
from auth.application.services.tokens import TokenService
from auth.application.services.users import UserService
from auth.domain.schemas import TokenGet
from auth.domain.schemas.users import UserGet, UserCreate, UserLogin

router = APIRouter(prefix='/auth/jwt', tags=['auth'])


@router.post('/register/',
             response_model=UserGet,
             response_model_exclude_none=True,
             status_code=status.HTTP_201_CREATED,
             responses=RESPONSE_USER_GET_EXAMPLE)
async def create_user(
        uow: UoWDep,
        user: UserCreate = Body(..., example=BODY_USER_CREATE_EXAMPLE),
):
    """
    Регистрация пользователя.

     - **username** - юзернейм

     - **email** - почта

     - **password** - пароль (длина пароля больше или равна 8 символам)

     **username**, **email**, **password** являются обязательными.
    """
    try:
        return await UserService().register_user(uow, user)
    except (exceptions.InvalidUsernameException,
            exceptions.InvalidEmailException) as error:
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
    except (exceptions.InvalidDataException,
            exceptions.EmptyDataException,
            exceptions.InvalidPasswordException) as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'{error}',
            headers={"WWW-Authenticate": "Bearer"},
        )




@router.get('/me/',
            response_model=UserGet,
            response_model_exclude_none=True,
            responses=RESPONSE_USER_GET_EXAMPLE)
async def read_user_me(user: UserGet = Depends(get_current_active_user)):
    return user


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
