import uuid

from auth.token.domain.exceptions.token import InvalidDataException
from auth.user.domain.exceptions.user import (
    InvalidEmailException,
    InvalidUsernameException,
)


class TokenService:
    async def check_username_and_email(
            self,
            username: str | None = None,
            email: str | None = None
    ) -> None:
        if username is not None and email is not None:
            raise InvalidDataException(
                'Invalid data received: username and '
                'email transmitted at the same time.'
            )
        elif username is None and email is None:
            raise InvalidDataException(
                'Invalid data received: email or username field is empty.'
            )

    async def check_user(
            self,
            value: bool,
            username: str | None = None,
            email: str | None = None
    ) -> None:
        if not value and username:
            raise InvalidUsernameException(
                'A user with this username already exists.'
            )
        elif not value and email:
            raise InvalidEmailException(
                'A user with this E-mail already exists.'
            )

    async def create_refresh_token(self, username: str) -> uuid.UUID:
        return uuid.uuid5(uuid.uuid4(), username)
