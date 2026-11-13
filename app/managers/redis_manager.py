"""Redis manager for tokens"""
import redis
from app.core.config import settings

class RedisManager:
    def __init__(self, redis_url = settings.REDIS_URL):
        self._redis_url = redis.from_url(redis_url, decode_responses=True)

    def blacklist_token(self, token: str, duration: int):
        if duration > 0:
            self._redis_url.set(f"blacklist:{token}","revoked", duration)

    def is_blacklisted(self, token: str):
        return self._redis_url.exists(f"blacklist:{token}") == 1

    def next_asset_id(self):
        return self._redis_url.incr("counters:asset_id")