import datetime as dt
from zoneinfo import ZoneInfo

from auth.application.exceptions import UserBannedException
from auth.core.constants import TIMEZONE, DATETIME_BANNED_FORMAT


class BaseService:
    def _check_user_banned(self, datetime: dt.datetime) -> None:
        if (datetime.timestamp() >= dt.datetime.now(
                tz=ZoneInfo(TIMEZONE)
        ).timestamp()):
            raise UserBannedException(
                'Пользователь заблокирован до '
                f'{datetime.strftime(DATETIME_BANNED_FORMAT)}.'
            )
