import redis

from app.core.config import settings

def init_redis_client():
    return redis.from_url(settings.redis.url, decode_responses=True)
