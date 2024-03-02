from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


async def custom_exception_handler(
        _: Request,
        exc: RequestValidationError
):
    """
    Кастомное переопределение ошибки,
    связанной с валидацией данных.
    """
    data = []
    for error in exc.errors():
        if error.get('msg'):
            data.append(
                {'msg': error.get('msg').replace('Value error, ', '')}
            )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": data}),
    )
