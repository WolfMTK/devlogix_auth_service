from sqlalchemy import Table, Column, ForeignKey

from auth.adapters.sqlalchemy_db.models import Base

users_roles = Table(
    'users_roles',
    Base.metadata,
    Column('user_id', ForeignKey('users.id')),
    Column('role_id', ForeignKey('roles.id'))
)
