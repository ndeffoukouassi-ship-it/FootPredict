import redis.asyncio as redis
from app.core.config import settings
from typing import Optional
import json
import hashlib

redis_client: Optional[redis.Redis] = None

async def get_redis() -> redis.Redis:
    global redis_client
    if redis_client is None:
        redis_client = redis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)
    return redis_client

async def close_redis():
    global redis_client
    if redis_client:
        await redis_client.close()
        redis_client = None

def cache_key(*args, prefix: str = "fp") -> str:
    raw = ":".join(str(a) for a in args)
    hashed = hashlib.md5(raw.encode()).hexdigest()[:10]
    return f"{prefix}:{hashed}"

async def get_cache(key: str):
    client = await get_redis()
    data = await client.get(key)
    return json.loads(data) if data else None

async def set_cache(key: str, value, expire: int = 300):
    client = await get_redis()
    await client.set(key, json.dumps(value, default=str), ex=expire)
