from sqlalchemy import select

from app.application.protocols.repository import SQLAlchemyRepository
from app.domain.models import AccessToken, RefreshToken


class AccessTokenRepository(SQLAlchemyRepository):
    model = AccessToken

    async def check_token(self, token: str) -> bool:
        stmt = select(self.model).where(self.model.token == token).exists()
        return await self.session.scalar(select(stmt))


class RefreshTokenRepository(SQLAlchemyRepository):
    model = RefreshToken
