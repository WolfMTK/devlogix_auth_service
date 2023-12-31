from fastapi import FastAPI
from httpx import AsyncClient

from src.api import routers
from src.core.decorators import repeat_every

app = FastAPI()


@app.on_event("startup")
@repeat_every(10)
async def get_token():
    async with AsyncClient(app=app) as client:
        await client.get('/auth/jwt/token-clear-users/')


for router in routers:
    app.include_router(router)
