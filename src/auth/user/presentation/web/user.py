from collections.abc import Callable

from fastapi import APIRouter, Depends, status, Body, HTTPException

from auth.common.adapters.security.permissions import PermissionBearerProvider
from auth.common.application.protocols.permissions import BearerProvider
from auth.common.presentation.dependencies.password import get_hashed_password
from auth.user.application.create_user import UserCreate
from auth.user.application.update_user_me import UserUpdateDTO
from auth.user.domain.exceptions.user import (
    InvalidEmailException,
    InvalidUsernameException,
)
from auth.user.domain.models.user import UserResult, UserUpdate
from auth.user.openapi.create_user import (
    RESPONSE_USER_CREATE_EXAMPLE,
    BODY_USER_CREATE_EXAMPLE,
)
from auth.user.openapi.read_user_me import RESPONSE_USER_GET_EXAMPLE
from auth.user.openapi.update_user_me import (
    BODY_USER_UPDATE_ME_EXAMPLE,
    RESPONSE_USER_UPDATE_ME_EXAMPLE,
)
from auth.user.presentation.interactor_factory import UserInteractorFactory

router = APIRouter(prefix='/users', tags=['users'])


@router.post(
    '/',
    name='Register a new user',
    response_model=UserResult,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
    responses=RESPONSE_USER_CREATE_EXAMPLE
)
async def create_user(
        user: UserCreate = Body(..., example=BODY_USER_CREATE_EXAMPLE),
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
    user.password = hashed_password(user.password)
    try:
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
    response_model=UserResult,
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


@router.patch(
    '/',
    name='Update me',
    response_model=UserResult,
    response_model_exclude_none=True,
    responses=RESPONSE_USER_UPDATE_ME_EXAMPLE
)
async def update_user_me(
        user: UserUpdate = Body(..., example=BODY_USER_UPDATE_ME_EXAMPLE),
        ioc: UserInteractorFactory = Depends(),
        bearer: BearerProvider = Depends(PermissionBearerProvider),
        hashed_password: Callable[[str | bytes], str] = Depends(
            get_hashed_password
        ),
):
    """
    Update your details

    * **username** - optional field

    * **email** - optional field

    * **password** - optional field
    """
    if user.password is not None:
        user.password = hashed_password(user.password)
    user_id = (await bearer.get_user()).id
    try:
        async with ioc.update_user_me() as update_user_me_interactor:
            return await update_user_me_interactor(
                UserUpdateDTO(
                    id=user_id,
                    value=user
                )
            )
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
