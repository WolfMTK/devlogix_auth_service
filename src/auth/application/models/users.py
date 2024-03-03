import uuid

from pydantic import BaseModel, EmailStr, field_validator, Field, ConfigDict
from pydantic.alias_generators import to_camel

from auth.core.validations import PasswordValidate, UsernameValidate


class UserBase(BaseModel):
    """Базовая схема пользователей."""
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True
    )

    username: str | None = Field(
        None, max_length=120, description='Юзернейм'
    )
    email: EmailStr | None = Field(
        None, min_length=6, max_length=255, description='E-mail'
    )


class UserCreate(BaseModel):
    """Схема регистрации пользователя."""
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True
    )

    username: str = Field(
        ..., max_length=120, description='Юзернейм'
    )
    email: EmailStr = Field(
        ..., min_length=6, max_length=255, description='E-mail'
    )
    password: str = Field(..., description='Пароль')

    @field_validator('password')
    @classmethod
    def check_password(cls, password: str) -> str:
        """Проверка пароля."""
        password_validate = PasswordValidate(password)
        password_validate.validate()
        return password

    @field_validator('username')
    @classmethod
    def check_username(cls, username: str) -> str:
        """Проверка юзернейма."""
        username_validate = UsernameValidate(username)
        username_validate.validate()
        return username


class UserLogin(UserBase):
    username: str | None = Field(None, description='Юзернейм')
    password: str = Field(..., description='Пароль')


class UserGet(UserBase):
    """Схема получения пользователя."""
    id: uuid.UUID | None = Field(
        None,
        description='Уникальный индентификатор пользователя'
    )
    first_name: str | None = Field(None, description='Имя')
    last_name: str | None = Field(None, description='Фамилия')
    is_active: bool | None = Field(None, description='Статус пользователя')


class UserUpdate(UserBase):
    """Схема обновления пользователя."""
    password: str | None = Field(None, description='Пароль')
    first_name: str | None = Field(None, description='Имя')
    last_name: str | None = Field(None, description='Фамилия')

    @field_validator('password')
    @classmethod
    def check_password(cls, password: str) -> str:
        """Проверка пароля."""
        password_validate = PasswordValidate(password)
        password_validate.validate()
        return password

    @field_validator('username')
    @classmethod
    def check_username(cls, username: str) -> str:
        """Проверка юзернейма."""
        username_validate = UsernameValidate(username)
        username_validate.validate()
        return username
