from typing import Any

from email_validator import validate_email, EmailNotValidError

from auth.core.constants import EMAIL_LENGTH
from auth.user.adapters.database.models import User
from auth.user.domain.exceptions.user import (
    InvalidEmailException,
    InvalidUsernameException,
)
from auth.user.domain.models.user import UserUpdate


class UserService:
    def check_email_exists(self, value: bool) -> None:
        if value:
            raise InvalidEmailException(
                'A user with this E-mail already exists.'
            )

    def check_email(self, email: str) -> None:
        # TODO: Temporal check of email length with constant
        if len(email) > EMAIL_LENGTH:
            raise ValueError('The allowed length for E-mail is exceeded.')
        try:
            validate_email(email, check_deliverability=False)
        except EmailNotValidError:
            raise ValueError('The value for the email field is invalid.')

    def check_username_exists(self, value: bool) -> None:
        if value:
            raise InvalidUsernameException(
                'A user with this username already exists.'
            )

    def set_is_active_user(self, user: User) -> None:
        user.is_active = True

    def update_user(self, user: UserUpdate) -> dict[str, Any]:
        data = dict()
        for key, value in vars(user).items():
            if value is not None:
                data[key] = value
        return data
