from app.application.protocols.unit_of_work import UoW
from app.core.http_error import error_400_handler
from app.core.password import get_password_hash
from app.domain.models import User
from app.domain.schemas.users import UserCreate, UserGet


class UserService:
    async def register_user(self, uow: UoW, user: UserCreate) -> User:
        async with uow:
            if await self._check_username_exists(uow, user.username):
                error_400_handler(
                    'Пользователь с таким юзернеймом уже существует!'
                )
            elif await self._check_email_exists(uow, user.email):
                error_400_handler(
                    'Пользователь с такой почтой уже существует!'
                )
            user.password = get_password_hash(user.password)
            user = await uow.users.add_one(**user.model_dump())
            await uow.commit()
            return user

    async def get_user(self, uow: UoW, username: str) -> UserGet:
        async with uow:
            user = await uow.users.find_one(username=username)
            return user.to_read_model()

    async def _check_username_exists(self, uow: UoW, username: str) -> bool:
        return await uow.users.get_user_exists(username=username)

    async def _check_email_exists(self, uow: UoW, email: str) -> bool:
        return await uow.users.get_user_exists(email=email)
