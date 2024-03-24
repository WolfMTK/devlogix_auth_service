from auth.user.adapters.database.models import User
from auth.user.domain.exceptions.user import (
    InvalidEmailException,
    InvalidUsernameException, EmptyUsernameException, InactiveUserException,
)


class UserService:
    def get_user_me(self, user: User | None) -> User:
        if user is None:
            raise EmptyUsernameException(
                'Invalid authentication credentials.'
            )
        return user

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
