from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from auth.token.adapters.database.models import Token
from auth.token.adapters.stub_db import StubTokenGateway


class TokenGateway(StubTokenGateway):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_token(self, token: Token) -> Token:
        pass

    async def check_user(
            self,
            username: str | None = None,
            email: str | None = None
    ) -> bool:
        stmt = select(Token).where(
            or_(
                Token.user.has(username=username),
                Token.user.has(email=email)
            )
        ).exists()
        return await self.session.scalar(select(stmt))
