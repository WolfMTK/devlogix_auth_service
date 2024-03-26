from collections.abc import Callable

from fastapi import APIRouter, Depends, status, Body, HTTPException

from auth.common.adapters.security.permissions import PermissionBearerProvider
from auth.common.application.protocols.permissions import BearerProvider
from auth.common.presentation.dependencies.password import get_hashed_password
from auth.user.application.create_user import UserDTO
from auth.user.domain.exceptions.user import (
    InvalidEmailException,
    InvalidUsernameException,
)
from auth.user.domain.models.user import UserResultDTO
from auth.user.openapi.create_user import (
    RESPONSE_USER_CREATE_EXAMPLE,
    BODY_USER_CREATE_EXAMPLE,
)
from auth.user.openapi.get_user_me import RESPONSE_USER_GET_EXAMPLE
from auth.user.presentation.interactor_factory import UserInteractorFactory

router = APIRouter(prefix='/users', tags=['users'])


@router.post(
    '/',
    name='Register a new user',
    response_model=UserResultDTO,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
    responses=RESPONSE_USER_CREATE_EXAMPLE
)
async def create_user(
        user: UserDTO = Body(..., example=BODY_USER_CREATE_EXAMPLE),
        ioc: UserInteractorFactory = Depends(),
        hashed_password: Callable[[str | bytes], str] = Depends(
            get_hashed_password
        ),
):
    """
    Register a new user.

    - **username** - required field

    - **email** - required field

    - **password** - required field
    """
    try:
        user.password = hashed_password(user.password)
        async with ioc.create_user() as create_user_interactor:
            return await create_user_interactor(user)
    except (InvalidEmailException, InvalidUsernameException) as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(error)
        )


@router.get(
    '/me/',
    name='About me',
    response_model=UserResultDTO,
    response_model_exclude_none=True,
    responses=RESPONSE_USER_GET_EXAMPLE
)
async def read_user_me(
        ioc: UserInteractorFactory = Depends(),
        bearer: BearerProvider = Depends(PermissionBearerProvider)
):
    """About me."""
    user = await bearer.get_user()
    async with ioc.get_user_me() as get_user_me_interactor:
        return await get_user_me_interactor(user)
