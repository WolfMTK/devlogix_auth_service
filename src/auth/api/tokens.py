from typing import Annotated

from fastapi import APIRouter, status, Body, HTTPException, Depends, Response
from redis.asyncio.client import Pipeline, AbstractRedis

from auth.api.permissions import get_current_active_user
from auth.application import exceptions
from auth.application.models import TokenGet, TokenUpdate, UserLogin, UserGet
from auth.application.protocols.database import UoWDatabase
from auth.application.services.tokens import TokenService
from auth.openapi.requests import BODY_USER_LOGIN_EXAMPLE
from auth.openapi.response import (
    RESPONSE_LOGIN_EXAMPLE,
    RESPONSE_LOGOUT_EXAMPLE,
)

router = APIRouter(prefix='/auth/token', tags=['auth'])


@router.post(
    '/login/',
    name='Логин',
    response_model=TokenGet,
    status_code=status.HTTP_200_OK,
    responses=RESPONSE_LOGIN_EXAMPLE
)
async def login(
        redis: AbstractRedis = Depends(),
        uow: UoWDatabase = Depends(),
        user: UserLogin = Body(
            ...,
            openapi_examples=BODY_USER_LOGIN_EXAMPLE
        )
):
    """
    Получение токена.

    **username** - юзернейм

    **email** - почта

    **password** - пароль

    **username/email** и **password** являются обязательными.
    """
    redis: Pipeline = redis  # noqa
    try:
        return await TokenService().get_token(uow, redis, user)
    except (exceptions.InvalidDataException,
            exceptions.EmptyDataException,
            exceptions.InvalidPasswordException) as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'{error}'
        )


@router.post(
    '/update/access_token/',
    name='Обновление временного токена',
    response_model=TokenGet,
    responses=RESPONSE_LOGIN_EXAMPLE
)
async def update_access_token(
        token: TokenUpdate,
        redis: AbstractRedis = Depends(),
        uow: UoWDatabase = Depends(),
):
    """Обновление временного токена."""
    redis: Pipeline = redis  # noqa
    try:
        return await TokenService().update_access_token(uow, redis, token)
    except exceptions.InvalidTokenException as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'{error}'
        )


@router.post(
    '/update/refresh_token/',
    name='Обновление токена',
    response_model=TokenGet,
    responses=RESPONSE_LOGIN_EXAMPLE
)
async def update_refresh_token(
        token: TokenUpdate,
        redis: AbstractRedis = Depends(),
        uow: UoWDatabase = Depends(),
):
    """Обновление токена для обновления временного токена."""
    redis: Pipeline = redis  # noqa
    try:
        return await TokenService().update_refresh_token(uow, redis, token)
    except exceptions.InvalidTokenException as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'{error}'
        )


@router.post(
    '/logout/',
    name='Удаление токена',
    status_code=status.HTTP_204_NO_CONTENT,
    responses=RESPONSE_LOGOUT_EXAMPLE
)
async def logout(
        current_user: Annotated[
            UserGet, Depends(get_current_active_user)
        ],
        redis: AbstractRedis = Depends(),
        uow: UoWDatabase = Depends(),
):
    """Удаление токена."""
    redis: Pipeline = redis  # noqa
    await TokenService().delete_token(uow, redis, current_user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    '/',
    include_in_schema=False,
    dependencies=[Depends(get_current_active_user)]
)
async def check_user() -> dict[str, bool]:
    """Проверка пользователя."""
    return {'status': True}
