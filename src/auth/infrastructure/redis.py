import redis.asyncio as aioredis
from auth.core import Settings

def create_connect():
    return aioredis.from_url(Settings.redis).pipeline()
