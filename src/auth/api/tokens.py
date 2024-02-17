from typing import Annotated

from fastapi import APIRouter, status, Body, HTTPException, Depends, Response

from auth.api.auth import get_current_active_user
from auth.api.dependencies import UoWDep
from auth.api.swagger import (RESPONSE_LOGIN_EXAMPLE,
                              RESPONSE_LOGOUT_EXAMPLE,
                              BODY_USER_LOGIN_EXAMPLE)
from auth.application.services import exceptions
from auth.application.services.tokens import TokenService
from auth.domain.schemas import TokenGet
from auth.domain.schemas.users import UserGet, UserLogin

router = APIRouter(prefix='/auth/token', tags=['auth'])


@router.post('/login/',
             name='Логин',
             response_model=TokenGet,
             status_code=status.HTTP_200_OK,
             responses=RESPONSE_LOGIN_EXAMPLE)
async def login(uow: UoWDep,
                user: UserLogin = Body(...,
                                       openapi_examples=BODY_USER_LOGIN_EXAMPLE)):
    """
    Получение токена.

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
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'{error}'
        )


@router.post('/logout/',
             name='Удаление токена',
             status_code=status.HTTP_204_NO_CONTENT,
             responses=RESPONSE_LOGOUT_EXAMPLE)
async def logout(
        current_user: Annotated[
            UserGet, Depends(get_current_active_user)
        ],
        uow: UoWDep
):
    """Удаление токена."""
    await TokenService().delete_token(uow, current_user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
