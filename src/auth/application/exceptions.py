class AuthException(Exception):
    pass


class EmptyDataException(AuthException):
    """Empty data exception."""


class EmptyUserException(AuthException):
    """Empty user exception."""

    def __str__(self) -> str:
        return 'Пользователь не найден.'


class InvalidEmailException(AuthException):
    """Invalid email exception."""


class InvalidUsernameException(AuthException):
    """Invalid username exception."""


class InvalidPasswordException(AuthException):
    """Invalid password exception."""


class InvalidDataException(AuthException):
    """Invalid data exception."""


class InvalidTokenException(AuthException):
    """Invalid token exception."""

    def __str__(self) -> str:
        return 'Невалидный токен.'


class UserBannedException(AuthException):
    """User banned exception."""
