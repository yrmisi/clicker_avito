from functools import lru_cache

from redis.asyncio import Redis

from src.config import settings


@lru_cache
def get_redis() -> Redis:
    """ """
    return Redis(
        host=settings.redis_db.host,
        port=settings.redis_db.port,
        db=settings.redis_db.db,
        password=settings.redis_db.password,
    )
