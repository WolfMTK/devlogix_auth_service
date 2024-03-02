from enum import StrEnum


class RoleEnum(StrEnum):
    """
    Типы для ролей.

    superuser - пользователь с высшими правами;
    admin - администратор;
    moderator - модератор.
    """
    superuser = 'superuser'
    admin = 'admin'
    moderator = 'moderator'
