from fastapi import APIRouter, Depends, HTTPException, status, Body

from auth.common.adapters.security.permissions import PermissionBearerProvider
from auth.common.application.protocols.permissions import BearerProvider
from auth.token.application.create_token import TokenResultDTO, UserDTO
from auth.token.domain.exceptions.token import InvalidDataException
from auth.token.openapi.create_token import (
    BODY_USER_LOGIN_EXAMPLE,
    RESPONSE_LOGIN_EXAMPLE,
)
from auth.token.openapi.delete_token import RESPONSE_LOGOUT_EXAMPLE
from auth.token.presentation.interactor_factory import TokenInteractorFactory
from auth.user.domain.exceptions.user import (
    InvalidEmailException,
    InvalidUsernameException,
)

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post(
    '/login',
    name='Login',
    response_model=TokenResultDTO,
    responses=RESPONSE_LOGIN_EXAMPLE
)
async def login(
        user: UserDTO = Body(..., openapi_examples=BODY_USER_LOGIN_EXAMPLE),
        ioc: TokenInteractorFactory = Depends()
):
    """
    Get tokens.

    Shemas:

        1. Username

            * **username** - required field

            * **password** - required field

        2. Email

            * **email** - required field

            * **password** - required field
    """
    try:
        async with ioc.create_token() as create_token_interactor:
            return await create_token_interactor(user)
    except (InvalidEmailException,
            InvalidDataException,
            InvalidUsernameException) as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(error)
        )


@router.post(
    '/logout',
    name='Delete token',
    status_code=status.HTTP_204_NO_CONTENT,
    responses=RESPONSE_LOGOUT_EXAMPLE
)
async def logout(
        ioc: TokenInteractorFactory = Depends(),
        bearer: BearerProvider = Depends(PermissionBearerProvider)
) -> None:
    """Delete token."""
    user = await bearer.get_user()
    async with ioc.delete_token() as delete_token_interactor:
        await delete_token_interactor(user.id)
