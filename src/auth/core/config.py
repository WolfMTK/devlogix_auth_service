import os
from dataclasses import dataclass


@dataclass
class Settings:
    db_url: str = os.getenv('DB_URL', 'sqlite+aiosqlite:///db.db')
    secret_token: str = os.getenv('SECRET_TOKEN', 'token')
    algorithm: str = os.getenv('ALGORITHM', 'HS256')
    time_access_token: int = os.getenv('TIME_ACCESS_TOKEN', 10)
    time_refresh_token: int = os.getenv('TIME_REFRESH_TOKEN', 24 * 60 * 60)
