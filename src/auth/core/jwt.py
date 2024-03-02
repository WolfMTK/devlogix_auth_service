import jwt

from auth.core import Settings


def create_token(data: dict) -> str:
    """Создание JWT токена."""
    to_encode = data.copy()
    return jwt.encode(
        to_encode,
        Settings.secret_token,
        algorithm=Settings.algorithm
    )


def decode_token(token: str) -> dict:
    """Декодирование JWT токена."""
    return jwt.decode(
        token,
        Settings.secret_token,
        algorithms=[Settings.algorithm]
    )
