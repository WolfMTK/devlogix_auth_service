from sqlalchemy import Table, Column, String, UUID, Boolean
from sqlalchemy.orm import registry
import uuid

from auth.common.adapters.database.models import Base
from auth.user.domain.models.user import User

mapper_registry = registry()

user = Table(
    'user',
    Base.metadata,
    Column('id', UUID, primary_key=True, default=uuid.uuid4),
    Column('username', String(), nullable=False, index=True),
    Column('email', String(), nullable=False, index=True),
    Column('password', String(), nullable=False),
    Column('is_active', Boolean(), default=True, nullable=False)
)

mapper_registry.map_imperatively(User, user)
