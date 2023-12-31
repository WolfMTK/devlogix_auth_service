from pydantic import BaseModel, EmailStr, field_validator, Field, ConfigDict

from src.core.constants import LENGTH_PASSWORD, LENGTH_USERNAME


class UserBase(BaseModel):
    username: str | None = Field(None, min_length=6, max_length=120)
    email: EmailStr | None = Field(None, min_length=6, max_length=255)


class UserCreate(BaseModel):
    """Схема регистрации пользователя."""
    username: str = Field(..., min_length=6, max_length=120)
    email: EmailStr = Field(..., min_length=6, max_length=255)
    password: str

    @field_validator('password')
    @classmethod
    def check_password(cls, password: str) -> str:
        if len(password) < LENGTH_PASSWORD:
            raise ValueError('Длина пароля меньше 8 символов!')
        return password

    @field_validator('username')
    @classmethod
    def check_username(cls, username: str) -> str:
        if len(username) < LENGTH_USERNAME:
            raise ValueError('Юзернейм меньше 6 символов!')
        return username


class UserLogin(UserBase):
    password: str


class UserGet(UserBase):
    """Схема получения пользователя."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str | None = None
    last_name: str | None = None
    is_active: bool
