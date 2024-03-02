from auth.adapters.sqlalchemy_db.base import SQLAlchemyRepository
from auth.adapters.sqlalchemy_db.models import Tokens


class TokenRepository(SQLAlchemyRepository):
    model = Tokens
