from typing import Sequence

from sqlalchemy import select, and_, or_

from auth.adapters.sqlalchemy_db.base import SQLAlchemyRepository
from auth.domain.models import User


class UserRepository(SQLAlchemyRepository):
    model = User

    async def get_user(self, username: str, email: str) -> User | None:
        stmt = (select(self.model)
                .where(or_(self.model.username == username,
                           self.model.email == email)))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_exists(self, **filter_by: dict[str, str]) -> bool:
        stmt = (select(self.model)
                .where(self.model.is_active == True)  # noqa: E712
                .filter_by(**filter_by).exists())
        return await self.session.scalar(select(stmt))

    async def check_username_user(self, id: int, username: str) -> bool:
        stmt = (select(self.model)
                .filter(and_(self.model.id != id,
                             self.model.username == username))
                .exists())
        return await self.session.scalar(select(stmt))

    async def check_email_user(self, id: int, email: str) -> bool:
        stmt = (select(self.model)
                .filter(and_(self.model.id != id,
                             self.model.email == email))
                .exists())
        return await self.session.scalar(select(stmt))

    async def get_users(self,
                        skip: int,
                        limit: int,
                        **filter_by: dict[str, str]) -> Sequence[User]:
        stmt = (select(self.model)
                .filter_by(**filter_by)
                .limit(limit)
                .offset(skip))
        result = await self.session.execute(stmt)
        return result.scalars().all()
