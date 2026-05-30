import json
from typing import Optional

import redis.asyncio as aioredis

from app.core.config import settings
from app.schemas.sensor import SensorReadingCreate


async def get_redis() -> aioredis.Redis:
    return aioredis.from_url(settings.REDIS_URL, decode_responses=True)


async def cache_latest_reading(reading: SensorReadingCreate) -> None:
    """Cache the latest reading per field in Redis for sub-millisecond dashboard reads."""
    redis = await get_redis()
    key = f"latest_reading:{reading.field_id}"
    await redis.setex(
        key,
        3600,  # 1 hour TTL
        json.dumps(reading.model_dump()),
    )
    await redis.aclose()


async def get_cached_reading(field_id: str) -> Optional[dict]:
    redis = await get_redis()
    key = f"latest_reading:{field_id}"
    raw = await redis.get(key)
    await redis.aclose()
    if raw:
        return json.loads(raw)
    return None


async def push_to_stream(reading_dict: dict) -> None:
    """Push raw sensor payload to Redis Stream for Kafka bridge consumption."""
    redis = await get_redis()
    await redis.xadd(
        "sensor_stream",
        {"data": json.dumps(reading_dict)},
        maxlen=10_000,
    )
    await redis.aclose()
