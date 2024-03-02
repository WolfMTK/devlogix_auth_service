from auth.adapters.sqlalchemy_db.base import SQLAlchemyRepository
from auth.domain.models import Token


class TokenRepository(SQLAlchemyRepository):
    model = Token
