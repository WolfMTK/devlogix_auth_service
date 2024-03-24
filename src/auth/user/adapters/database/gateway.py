from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.user.adapters.database.models import User
from auth.user.adapters.stub_db import StubUserGateway


class UserGateway(StubUserGateway):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_user(self, user: User) -> None:
        self.session.add(user)

    async def check_user(self, **filter_by: Any) -> bool:
        stmt = select(User).where(
            User.is_active == True
        ).filter_by(
            **filter_by
        ).exists()
        return await self.session.scalar(select(stmt))

    async def get_user(self, **filter_by: Any) -> User | None:
        stmt = select(User).filter_by(**filter_by)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
