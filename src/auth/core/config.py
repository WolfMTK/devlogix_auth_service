import os
from dataclasses import dataclass


@dataclass
class Settings:
    """Настройки для приложения."""

    db_url: str = os.getenv(
        'DB_URL',
        'sqlite+aiosqlite:///db.db'
    )
    secret_token: str = os.getenv('SECRET_TOKEN', 'token')
    algorithm: str = os.getenv('ALGORITHM', 'HS256')
    redis: str = os.getenv('REDIS_URL', 'redis://localhost')
    time_access_token: str = os.getenv('TIME_ACCESS_TOKEN', 24 * 60 * 60)
    time_refresh_token: str = os.getenv('TIME_REFRESH_TOKEN', 24 * 60 * 60)
