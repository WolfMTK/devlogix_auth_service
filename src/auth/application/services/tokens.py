import datetime as dt
from uuid import uuid5, uuid4

from redis.asyncio.client import Pipeline

from auth.adapters.sqlalchemy_db.models import Token, User
from auth.application.exceptions import (
    InvalidDataException,
    EmptyDataException,
    InvalidPasswordException,
    InvalidTokenException,
)
from auth.application.models import UserLogin, TokenGet, TokenUpdate
from auth.application.protocols.database import UoWDatabase
from auth.core import Settings
from auth.core.jwt import create_token
from auth.core.password import verify_password


class TokenService:
    def __init__(self):
        self._time_access_token = dt.timedelta(
            minutes=int(Settings.time_access_token)
        )

    async def get_token(
            self,
            uow: UoWDatabase,
            redis: Pipeline,
            schema: UserLogin
    ) -> TokenGet:
        """Получение токена."""
        async with uow:
            user = await self._check_user_correct_data(uow, schema)
            access_token = self._create_access_token(
                user.username,
                self._time_access_token
            )
            refresh_token = self._create_refresh_token(user.username)
            if user.token:
                user.token.name = refresh_token
            else:
                user.token = Token(name=refresh_token)
            await uow.commit()
            await redis.set(
                f'access-token::{user.id}', access_token,
                ex=self._time_access_token
            )
            await redis.execute()
            return TokenGet(
                access_token=access_token,
                expires_in=self._time_access_token.total_seconds(),
                refresh_token=refresh_token,
                token_type='Bearer'
            )

    async def update_access_token(
            self,
            uow: UoWDatabase,
            redis: Pipeline,
            schema: TokenUpdate
    ) -> TokenGet:
        """Обновление временного токена."""
        async with uow:
            token = await uow.tokens.find_one(name=schema.refresh_token)
            if not token:
                raise InvalidTokenException()
            access_token = self._create_access_token(
                token.user.username,
                self._time_access_token
            )
            await self._update_access_token(
                redis,
                token.user_id,
                access_token,
                self._time_access_token
            )
            return TokenGet(
                access_token=access_token,
                expires_in=self._time_access_token.total_seconds(),
                refresh_token=token.name,
                token_type='Bearer'
            )

    async def update_refresh_token(
            self,
            uow: UoWDatabase,
            redis: Pipeline,
            schema: TokenUpdate
    ) -> TokenGet:
        """Обновление токена для обновления временного токена."""
        async with uow:
            token = await uow.tokens.find_one(name=schema.refresh_token)
            if not token:
                raise InvalidTokenException()
            username = token.user.username
            token.name = self._create_refresh_token(username)
            access_token = self._create_access_token(
                username,
                self._time_access_token
            )
            await uow.commit()
            await self._update_access_token(
                redis,
                token.user_id,
                access_token,
                self._time_access_token
            )
            return TokenGet(
                access_token=access_token,
                expires_in=self._time_access_token.total_seconds(),
                refresh_token=token.name,
                token_type='Bearer'
            )

    async def delete_token(
            self,
            uow: UoWDatabase,
            redis: Pipeline,
            id: int
    ) -> None:
        """Удаление токена."""
        async with uow:
            await uow.tokens.delete_one(user_id=id)
            await uow.commit()
            await redis.delete(f'access-token::{id}')
            await redis.execute()

    def _create_access_token(self, username: str, time: dt.timedelta) -> str:
        access_token = create_token(
            data={'sub': username,
                  'date': str(dt.datetime.now() + time)},
        )
        return access_token

    def _create_refresh_token(self, username: str) -> str:
        return str(uuid5(uuid4(), username))

    async def _update_access_token(
            self,
            redis: Pipeline,
            user_id: int,
            access_token: str,
            time_access_token: dt.timedelta
    ) -> None:
        await redis.delete(f'access-token::{user_id}')
        await redis.set(
            f'access-token::{user_id}', access_token, ex=time_access_token
        )
        await redis.execute()

    async def _check_user_correct_data(
            self, uow: UoWDatabase,
            schema: UserLogin
    ) -> User:
        if schema.username and schema.email:
            raise InvalidDataException('Введите username или email.')

        if schema.username:
            user = await uow.users.find_one(username=schema.username)
        elif schema.email:
            user = await uow.users.find_one(email=schema.email)
        else:
            raise EmptyDataException('Отсутствует username или email.')

        if user and verify_password(schema.password, user.password):
            return user
        raise InvalidPasswordException('Пароль или логин введен неверно.')
