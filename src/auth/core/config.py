import os
from dataclasses import dataclass


@dataclass
class Settings:
    db_url: str = os.getenv(
        'DB_URL',
        'postgresql+asyncpg://postgres:password@localhost:5432/users'
    )
    secret_token: str = os.getenv('SECRET_TOKEN', 'token')
    algorithm: str = os.getenv('ALGORITHM', 'HS256')
    time_access_token: int = os.getenv('TIME_ACCESS_TOKEN', 24 * 60 * 60)
    time_refresh_token: int = os.getenv('TIME_REFRESH_TOKEN', 24 * 60 * 60)
