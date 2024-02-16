from .constants import LENGTH_PASSWORD, PATTERN_PASSWORD, LENGTH_USERNAME
import re


class PasswordValidate:
    """Валидатор для паролей."""

    def __init__(self, password: str) -> None:
        self._password = password

    def validate(self) -> None:
        """Валидация пароля."""
        self._check_length_password()
        self._check_password_pattern()

    def _check_length_password(self) -> None:
        if len(self._password) < LENGTH_PASSWORD:
            raise ValueError('Длина пароля меньше 8 символов.')

    def _check_password_pattern(self) -> None:
        if not re.match(PATTERN_PASSWORD, self._password):
            raise ValueError(
                'Пароль должен содержать: '
                'минимум одну цифру; '
                'по крайней мере один алфавит верхнего регистра; '
                'по крайней мере один алфавит нижнего регистра; '
                'по крайней мере один специальный символ, '
                'который включает в себя !#$%&()*+,-./:;<=>?@[\]^_`{|}~.'
            )


class UsernameValidate:
    """Валидатор для юзернеймов."""

    def __init__(self, username: str) -> None:
        self._username = username

    def validate(self) -> None:
        self._check_length_username()

    def _check_length_username(self) -> None:
        if len(self._username) < LENGTH_USERNAME:
            raise ValueError('Юзернейм меньше 6 символов.')
