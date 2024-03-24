from fastapi import APIRouter, Depends, HTTPException, status

from auth.token.application.create_token import TokenResultDTO, UserDTO
from auth.token.domain.exceptions.token import InvalidDataException
from auth.token.presentation.interactor_factory import TokenInteractorFactory
from auth.user.domain.exceptions.user import (
    InvalidEmailException,
    InvalidUsernameException,
)

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post(
    '/login',
    name='Login',
    response_model=TokenResultDTO
)
async def login(
        user: UserDTO,
        ioc: TokenInteractorFactory = Depends()
):
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
