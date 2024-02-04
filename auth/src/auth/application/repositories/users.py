from sqlalchemy import select

from auth.application.protocols.repository import SQLAlchemyRepository
from auth.domain.models.users import User


class UserRepository(SQLAlchemyRepository):
    model = User

    async def get_user_exists(self, **filter_by: dict[str, str]) -> bool:
        stmt = select(self.model).filter_by(**filter_by).exists()
        return await self.session.scalar(select(stmt))
