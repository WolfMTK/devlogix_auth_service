from typing import Annotated

from fastapi import Depends
from redis.asyncio.client import Pipeline

from auth.infrastructure.redis import create_connect

RedisConnect = Annotated[Pipeline, Depends(create_connect)]
