from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class TokenBase(BaseModel):
    """Базовая схема токенов."""
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True
    )

    refresh_token: str = Field(..., description='Токен обновления')


class TokenGet(TokenBase):
    """Схема получения токенов."""
    access_token: str = Field(..., description='Временный токен')
    expires_in: int = Field(..., description='Время действия токена')
    token_type: str = Field(..., description='Тип токена')


class TokenData(BaseModel):
    """Сериализация данных."""
    username: str | None = None


class TokenUpdate(TokenBase):
    """Схема обновления токена."""
