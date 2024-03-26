import uuid

from email_validator import EmailNotValidError, validate_email

from auth.core.constants import EMAIL_LENGTH
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
        elif email is not None:
            # TODO: Temporal check of email length with constant
            if len(email) > EMAIL_LENGTH:
                raise ValueError('The allowed length for E-mail is exceeded.')
            try:
                validate_email(email, check_deliverability=False)
            except EmailNotValidError:
                raise ValueError('The value for the email field is invalid.')

    async def check_user(
            self,
            value: bool,
            username: str | None = None,
            email: str | None = None
    ) -> None:
        if not value and username:
            raise InvalidUsernameException(
                'The data was entered incorrectly.'
            )
        elif not value and email:
            raise InvalidEmailException(
                'The data was entered incorrectly.'
            )

    async def create_refresh_token(self, username: str) -> uuid.UUID:
        return uuid.uuid5(uuid.uuid4(), username)
