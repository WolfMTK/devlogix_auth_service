import datetime as dt

LENGTH = 5


async def check_date(date: dt.datetime) -> bool:
    return date > dt.datetime.utcnow()


async def correct_format_date(date_list: list) -> dt.datetime:
    if not isinstance(date_list, list):
        raise ValueError
    for index, date in enumerate(date_list):
        if len(date) == 1:
            date_list[index] = f'0{date}'
    date_str = ''.join(date_list[0:3][::-1]) + 'T' + ''.join(date_list[3:])
    date = dt.datetime.fromisoformat(date_str)
    if not await check_date(date):
        raise ValueError
    return date


async def get_correct_date(time: dt.timedelta) -> str:
    days = time.days
    hours = str(time.seconds // 3600)
    minutes = str((time.seconds // 60) % 60)
    seconds = str(time.seconds % 60)
    if len(hours) != 2:
        hours = '0' + hours
    if len(minutes) != 2:
        minutes = '0' + minutes
    if len(seconds) != 2:
        seconds = '0' + seconds
    return f'{days} {hours}:{minutes}:{seconds}'
