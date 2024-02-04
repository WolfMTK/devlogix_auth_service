from auth.application.protocols.repository import SQLAlchemyRepository
from auth.domain.models import Token


class TokenRepository(SQLAlchemyRepository):
    model = Token
