from pydantic import PostgresDsn, SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: PostgresDsn
    secret_token: SecretStr
    algorithm: str
    time_access_token: int
    time_refresh_token: int

    class Config:
        env_file = '.env'
