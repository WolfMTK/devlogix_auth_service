import uuid

from sqlalchemy import select, or_, and_, delete
from sqlalchemy.ext.asyncio import AsyncSession

from auth.token.adapters.database.models import Token
from auth.token.adapters.stub_db import StubTokenGateway
from auth.user.adapters.database.models import User


class TokenGateway(StubTokenGateway):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_token(self, user: User, token: uuid.UUID) -> Token:
        if user.token is None:
            user.token = Token(name=str(token))
        else:
            user.token.name = str(token)
        return user.token

    async def get_user(self, username: str, email: str) -> User:
        stmt = select(User).where(
            or_(
                User.username == username,
                User.email == email
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar()

    async def check_user(
            self,
            username: str | None = None,
            email: str | None = None
    ) -> bool:
        stmt = select(User).where(
            and_(
                or_(
                    User.username == username,
                    User.email == email
                ),
                User.is_active == True
            )
        ).exists()
        return await self.session.scalar(select(stmt))

    async def delete_token(self, user_id: uuid.UUID) -> None:
        stmt = delete(Token).where(Token.user_id == user_id)
        await self.session.execute(stmt)
