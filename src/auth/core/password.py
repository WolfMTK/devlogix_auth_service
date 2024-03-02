from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(plain_password, hashed_password) -> bool:
    """Проверка захешированного пароля."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password) -> str:
    """Получения хеша из пароля."""
    return pwd_context.hash(password)
