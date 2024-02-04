import asyncio
import logging
from functools import wraps
from traceback import format_exception
from typing import Callable, Coroutine, Any, Union

from starlette.concurrency import run_in_threadpool

_F = Callable[[], None]
_P = Callable[[], Coroutine[Any, Any, None],]
_T = Callable[[Union[_F, _P]], _P]


def repeat_every(seconds: float,
                 logger: logging.Logger | None = None) -> _F:
    def decorator(func: _F | _P) -> _P:
        is_coroutine = asyncio.iscoroutinefunction(func)

        @wraps(func)
        async def wrapped() -> None:
            async def loop() -> None:
                while True:
                    try:
                        if is_coroutine:
                            await func()
                        else:
                            await run_in_threadpool(func)
                    except Exception as exc:
                        if logger is not None:
                            formatted_exception = ''.join(
                                format_exception(type(exc), exc,
                                                 exc.__traceback__)
                            )
                            logger.error(formatted_exception)
                    await asyncio.sleep(seconds)

            asyncio.ensure_future(loop())

        return wrapped

    return decorator
