from fastapi import APIRouter, status, Body, HTTPException, Depends

from auth.api.dependencies import UoWDep
from auth.api.swagger import (RESPONSE_USER_CREATE_EXAMPLE,
                              BODY_USER_CREATE_EXAMPLE,
                              RESPONSE_USER_GET_EXAMPLE)
from auth.application.services import exceptions
from auth.application.services.users import UserService
from auth.domain.schemas.users import UserGet, UserCreate
from .auth import get_current_active_user

router = APIRouter(prefix='/users', tags=['users'])


@router.post('/',
             name='Регистраци пользователя',
             response_model=UserGet,
             response_model_exclude_none=True,
             status_code=status.HTTP_201_CREATED,
             responses=RESPONSE_USER_CREATE_EXAMPLE)
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


@router.get('/me/',
            name='Данные о себе',
            response_model=UserGet,
            response_model_exclude_none=True,
            responses=RESPONSE_USER_GET_EXAMPLE)
async def read_user_me(user: UserGet = Depends(get_current_active_user)):
    return user
