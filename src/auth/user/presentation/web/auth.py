from fastapi import APIRouter, Depends, HTTPException, status, Body

from auth.token.application.create_token import TokenResultDTO, UserDTO
from auth.token.domain.exceptions.token import InvalidDataException
from auth.token.openapi.create_tokens import (
    BODY_USER_LOGIN_EXAMPLE,
    RESPONSE_LOGIN_EXAMPLE,
)
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
