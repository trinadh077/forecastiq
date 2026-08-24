from typing import Optional
import redis.asyncio as aioredis
from app.config.settings import settings
from app.config.logging import logger

class RedisService:
    def __init__(self):
        self.redis: Optional[aioredis.Redis] = None

    async def connect(self):
        try:
            self.redis = aioredis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True
            )
            await self.redis.ping()
            logger.info("Connected to Redis server successfully.")
        except Exception as e:
            logger.warning(f"Could not connect to Redis: {e}. Falling back to in-memory mode if needed.")
            self.redis = None

    async def close(self):
        if self.redis:
            await self.redis.close()

    async def blacklist_token(self, token: str, expire_seconds: int = 86400) -> bool:
        if not self.redis:
            return True
        try:
            await self.redis.setex(f"blacklist:{token}", expire_seconds, "true")
            return True
        except Exception as e:
            logger.error(f"Error blacklisting token in Redis: {e}")
            return False

    async def is_token_blacklisted(self, token: str) -> bool:
        if not self.redis:
            return False
        try:
            val = await self.redis.get(f"blacklist:{token}")
            return val is not None
        except Exception as e:
            logger.error(f"Error checking token blacklist in Redis: {e}")
            return False

redis_service = RedisService()
