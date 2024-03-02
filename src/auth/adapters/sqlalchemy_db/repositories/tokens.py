from auth.adapters.sqlalchemy_db.base import SQLAlchemyRepository
from auth.adapters.sqlalchemy_db.models import Token


class TokenRepository(SQLAlchemyRepository):
    model = Token
