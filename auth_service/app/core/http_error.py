from . import exceptions


def error_404_handler(message: str):
    raise exceptions.HTTPError404(message)


def error_401_handler(message: str):
    raise exceptions.HTTPError401(message)


def error_400_handler(message: str):
    raise exceptions.HTTPError400(message)
