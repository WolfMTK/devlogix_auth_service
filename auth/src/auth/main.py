from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from auth.api import routers

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def custom_exception_handler(_: Request, exc: RequestValidationError):
    data = []
    for error in exc.errors():
        if error.get('msg'):
            data.append({'msg': error.get('msg').replace('Value error, ', '')})
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": data}),
    )


for router in routers:
    app.include_router(router)
