import datetime as dt
from uuid import uuid5, uuid4

from auth.application.protocols.unit_of_work import UoW
from auth.core import Settings
from auth.core.jwt import create_token
from auth.core.password import verify_password
from auth.domain.models import User, Token
from auth.domain.schemas import UserLogin, TokenGet
from .exceptions import InvalidDataException, EmptyDataException, InvalidPasswordException


class TokenService:
    async def get_token(self,
                        uow: UoW,
                        schema: UserLogin) -> TokenGet:
        async with uow:
            user = await self._check_user_correct_data(uow, schema)
            time_access_token = dt.timedelta(
                minutes=Settings.time_access_token
            )
            access_token = self._create_access_token(user.username,
                                                     time_access_token)
            refresh_token = self._create_refresh_token(user.username)
            if user.token:
                user.token.name = refresh_token
            else:
                user.token = Token(name=refresh_token)
            await uow.commit()
            return TokenGet(access_token=access_token,
                            expires_in=time_access_token.total_seconds(),
                            refresh_token=refresh_token,
                            token_type='Bearer')

    async def delete_token(self,
                           uow: UoW,
                           id: int):
        async with uow:
            await uow.token.delete_one(user_id=id)
            await uow.commit()

    def _create_access_token(self, username: str, time: dt.timedelta) -> str:
        access_token = create_token(
            data={'sub': username,
                  'date': str(dt.datetime.now() + time)},
            expires_delta=time
        )
        return access_token

    def _create_refresh_token(self, username: str) -> str:
        return str(uuid5(uuid4(), username))

    async def _check_user_correct_data(self, uow: UoW, schema: UserLogin) -> User:
        if schema.username and schema.email:
            raise InvalidDataException('Введите username или email!')

        if schema.username:
            user = await uow.users.find_one(username=schema.username)
        elif schema.email:
            user = await uow.users.find_one(email=schema.email)
        else:
            raise EmptyDataException('Отсутствует username или email!')
        if user and verify_password(schema.password, user.password):
            return user
        raise InvalidPasswordException('Пароль или логин введен неверно!')
