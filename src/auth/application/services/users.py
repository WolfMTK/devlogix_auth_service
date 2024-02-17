from auth.application.protocols.unit_of_work import UoW
from auth.application.services.exceptions import (InvalidEmailException,
                                                  InvalidUsernameException,
                                                  EmptyUserException)
from auth.core.password import get_password_hash
from auth.domain.models import User
from auth.domain.schemas.users import UserCreate, UserGet, UserUpdate


class UserService:
    async def register_user(self, uow: UoW, schema: UserCreate) -> UserGet:
        """Регистрация пользователя."""
        async with uow:
            if await self._check_username_exists(uow, schema.username):
                raise InvalidUsernameException(
                    'Пользователь с таким юзернеймом уже существует.'
                )
            elif await self._check_email_exists(uow, schema.email):
                raise InvalidEmailException(
                    'Пользователь с такой почтой уже существует.'
                )

            schema.password = get_password_hash(schema.password)
            user = await self._get_user(uow,
                                        username=schema.username,
                                        email=schema.email)

            if user:
                user.set_empty_attributes()
                await self._clear_token(uow, user)
                user.is_active = True
                for key, value in schema.model_dump().items():
                    setattr(user, key, value)
            else:
                user = await uow.users.add_one(**schema.model_dump())

            await uow.commit()
            return user.to_read_model()

    async def get_user(self, uow: UoW, username: str) -> UserGet:
        """Получение пользователя."""
        async with uow:
            if not (user := await uow.users.find_one(username=username)):
                raise EmptyUserException()
            if user.token:
                return user.to_read_model()
            raise EmptyUserException()

    async def get_users(self, uow: UoW, skip: int, limit: int) -> list[
        UserGet]:
        """Получение пользователей."""
        async with uow:
            users = await uow.users.get_users(skip, limit)
            return [user.to_read_model() for user in users]

    async def update_me(
            self, uow: UoW, user_id: int, schema: UserUpdate
    ) -> UserGet:
        """Обновление пользователя."""
        async with uow:
            if await self._check_user_username(uow, user_id, schema.username):
                raise InvalidUsernameException(
                    'Пользователь с таким юзернеймом уже существует.'
                )
            elif await self._check_user_email(uow, user_id, schema.email):
                raise InvalidEmailException(
                    'Пользователь с такой почтой уже существует.'
                )

            if schema.password:
                schema.password = get_password_hash(schema.password)
            user = await uow.users.update_one(
                user_id, **schema.model_dump(exclude_none=True)
            )
            await uow.commit()
            return user.to_read_model()

    async def delete_me(self, uow: UoW, user_id: int) -> None:
        """Удаление пользователя."""
        async with uow:
            user = await uow.users.find_one(id=user_id)
            user.is_active = False
            await uow.commit()

    async def _clear_token(self, uow: UoW, user: User) -> None:
        if user.token:
            await uow.token.delete_one(user_id=user.id)

    async def _get_user(self, uow: UoW, username: str, email: str) -> User:
        return await uow.users.get_user(username=username, email=email)

    async def _check_username_exists(self, uow: UoW, username: str) -> bool:
        return await uow.users.get_user_exists(username=username)

    async def _check_email_exists(self, uow: UoW, email: str) -> bool:
        return await uow.users.get_user_exists(email=email)

    async def _check_user_email(
            self, uow: UoW, id: int, email: str
    ) -> bool:
        return await uow.users.check_email_user(id, email)

    async def _check_user_username(
            self, uow: UoW, id: int, username: str
    ) -> bool:
        return await uow.users.check_username_user(id, username)
