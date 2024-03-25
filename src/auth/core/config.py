import os
from dataclasses import dataclass


class ConfigParseError(ValueError):
    pass


@dataclass
class TokenTime:
    time_access_token: str = os.getenv('TIME_ACCESS_TOKEN', '15')


@dataclass
class DatabaseConfig:
    db_uri: str


@dataclass
class JWTConfig:
    secret_token: str
    algorithm: str


def get_str_env(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise ConfigParseError(f'{key} is not set')
    return value


def load_database_config() -> DatabaseConfig:
    return DatabaseConfig(db_uri=get_str_env('DB_URI'))


def load_jwt_config() -> JWTConfig:
    return JWTConfig(
        secret_token=get_str_env('SECRET_TOKEN'),
        algorithm=get_str_env('ALGORITHM')
    )
