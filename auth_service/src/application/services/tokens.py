from datetime import timedelta, datetime
from uuid import uuid5, uuid4

from src.application.protocols.unit_of_work import UoW
from src.core import http_error, settings
from src.core.exceptions import InvalidDataError
from src.core.jwt import create_token
from src.core.password import verify_password
from src.domain.models import User, AccessToken, RefreshToken
from src.domain.schemas.tokens import TokenGet
from src.domain.schemas.users import UserLogin


class TokenService:
    async def get_token(self,
                        uow: UoW,
                        schema: UserLogin) -> TokenGet:
        async with uow:
            try:
                user = await self._check_user_correct_data(uow, schema)
            except (AttributeError, InvalidDataError):
                http_error.error_401_handler(
                    'Некорректный юзернейм/email или пароль!')
            token_time = timedelta(minutes=settings.time_access_token)
            access_token = self._create_access_token(user.username,
                                                     token_time)
            refresh_token = self._create_refresh_token(user.username)
            await self._add_token(user, access_token,
                                  self._create_refresh_token(user.username))
            await uow.commit()
            return TokenGet(access_token=access_token,
                            expires_in=token_time.total_seconds(),
                            refresh_token=refresh_token,
                            token_type='Bearer')

    async def delete_token(self, uow: UoW, user_id: int) -> None:
        async with uow:
            user = await uow.users.find_one(id=user_id)
            access_token = user.access_token
            refresh_token = user.refresh_token
            await uow.access_token.delete_one(id=access_token.id)
            await uow.refresh_token.delete_one(id=refresh_token.id)
            await uow.commit()

    async def clear_tokens(self, uow: UoW) -> None:
        async with uow:
            refresh_tokens = await uow.refresh_token.find_all()
            for refresh_token in refresh_tokens:
                date_token = refresh_token.created_at + timedelta(
                    minutes=settings.time_refresh_token
                )
                if self._check_date(date_token):
                    access_token = refresh_token.user.access_token
                    await uow.access_token.delete_one(id=access_token.id)
                    await uow.refresh_token.delete_one(id=refresh_token.id)
                    await uow.commit()

    async def check_token(self, uow: UoW, token: str) -> bool:
        async with uow:
            return await uow.access_token.check_token(token)

    def _create_access_token(self, username: str, time: timedelta) -> str:
        access_token = create_token(
            data={'sub': username,
                  'date': str(datetime.utcnow() + time)},
            expires_delta=time
        )
        return access_token

    def _create_refresh_token(self, username: str) -> str:
        return str(uuid5(uuid4(), username))

    def _check_date(self, date: datetime) -> bool:
        return date < datetime.utcnow()

    async def _add_token(self,
                         user: User,
                         access_token: str,
                         refresh_token: str) -> None:
        if user.access_token and user.refresh_token:
            user.access_token.token = access_token
            user.refresh_token.token = refresh_token
            user.refresh_token.created_at = datetime.utcnow()
        elif not user.access_token and not user.refresh_token:
            user.access_token = AccessToken(token=access_token)
            user.refresh_token = RefreshToken(token=refresh_token)

    async def _check_user_correct_data(self,
                                       uow: UoW,
                                       schema: UserLogin) -> User:
        if schema.username and schema.email:
            raise InvalidDataError('Invalid data')
        elif schema.username:
            user = await uow.users.find_one(username=schema.username)
        elif schema.email:
            user = await uow.users.find_one(email=schema.email)
        else:
            raise InvalidDataError('Invalid data')
        if verify_password(schema.password, user.password):
            return user
        raise InvalidDataError('Invalid password')
