from fastapi import APIRouter, status, Body, HTTPException, Depends

from auth.api.dependencies import UoWDep
from auth.api.swagger import (RESPONSE_USER_CREATE_EXAMPLE,
                              BODY_USER_CREATE_EXAMPLE,
                              RESPONSE_USER_GET_EXAMPLE,
                              BODY_USER_UPDATE_EXAMPLE,
                              RESPONSE_USER_UPDATE_EXAMPLE)
from auth.application.services import exceptions
from auth.application.services.users import UserService
from auth.domain.schemas.users import UserGet, UserCreate, UserUpdate
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


@router.patch('/',
              name='Обновления данных о себе',
              response_model=UserGet,
              response_model_exclude_none=True,
              responses=RESPONSE_USER_UPDATE_EXAMPLE)
async def update_user(
        uow: UoWDep,
        user: UserUpdate = Body(..., example=BODY_USER_UPDATE_EXAMPLE),
        current_user: UserGet = Depends(get_current_active_user)
):
    """
    Обновление данных о себе

    - **username** - юзернейм

    - **email** - почта

    - **password** - пароль

    - **first_name** - имя

    - **last_name** - фамилия

    Все поля являются не обязательными.
    """
    try:
        return await UserService().update_user(uow, current_user.id, user)
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
    """Данные о себе."""
    return user


@router.get('/',
            name='Пользователи',
            response_model=list[UserGet],
            response_model_exclude_none=True,
            dependencies=[Depends(get_current_active_user)])
async def read_users(uow: UoWDep,
                     skip: int = 0,
                     limit: int = 5):
    """Получение пользователей."""
    return await UserService().get_users(uow, skip, limit)

