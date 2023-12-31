import os

from pydantic import SecretStr, PostgresDsn, BaseModel


class Settings(BaseModel):
    bot_token: SecretStr = os.getenv('BOT_TOKEN')
    db_url: PostgresDsn = os.getenv('DB_URL')
    throttle_time_spin: int = os.getenv('THROTTLE_TIME_SPIN')
    throttle_time_other: int = os.getenv('THROTTLE_TIME_OTHER')
