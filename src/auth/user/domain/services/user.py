from auth.user.adapters.database.models import User
from auth.user.domain.exceptions.user import (
    InvalidEmailException,
    InvalidUsernameException,
    InactiveUserException,
)


class UserService:
    def check_email_exists(self, value: bool) -> None:
        if value:
            raise InvalidEmailException(
                'A user with this E-mail already exists.'
            )

    def check_username_exists(self, value: bool) -> None:
        if value:
            raise InvalidUsernameException(
                'A user with this username already exists.'
            )

    def check_is_active(self, user: User) -> None:
        if not user.is_active:
            raise InactiveUserException(
                'Invalid authentication credentials.'
            )

    def set_is_active_user(self, user: User) -> None:
        user.is_active = True
