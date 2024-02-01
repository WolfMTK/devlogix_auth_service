from models.users import Users
from .repository import SQLAlchemyRepository


class UsersRepository(SQLAlchemyRepository):
    model = Users
