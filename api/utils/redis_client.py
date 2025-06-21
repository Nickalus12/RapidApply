"""
Redis client utilities for caching and session management
"""

import redis.asyncio as redis
import json
import logging
from typing import Optional, Any

from api.config import settings

logger = logging.getLogger(__name__)

# Global Redis client
redis_client: Optional[redis.Redis] = None


async def init_redis():
    """Initialize Redis connection"""
    global redis_client
    try:
        redis_client = redis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True
        )
        # Test connection
        await redis_client.ping()
        logger.info("Redis connection established")
    except Exception as e:
        logger.error(f"Error connecting to Redis: {e}")
        raise


async def get_redis() -> redis.Redis:
    """Get Redis client instance"""
    if not redis_client:
        await init_redis()
    return redis_client


async def cache_set(
    key: str,
    value: Any,
    expire: Optional[int] = None
) -> bool:
    """Set cache value"""
    try:
        client = await get_redis()
        key = f"{settings.REDIS_PREFIX}{key}"
        
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        
        if expire is None:
            expire = settings.CACHE_TTL
            
        return await client.setex(key, expire, value)
    except Exception as e:
        logger.error(f"Error setting cache: {e}")
        return False


async def cache_get(key: str) -> Optional[Any]:
    """Get cache value"""
    try:
        client = await get_redis()
        key = f"{settings.REDIS_PREFIX}{key}"
        value = await client.get(key)
        
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        return None
    except Exception as e:
        logger.error(f"Error getting cache: {e}")
        return None


async def cache_delete(key: str) -> bool:
    """Delete cache value"""
    try:
        client = await get_redis()
        key = f"{settings.REDIS_PREFIX}{key}"
        return bool(await client.delete(key))
    except Exception as e:
        logger.error(f"Error deleting cache: {e}")
        return False


async def cache_exists(key: str) -> bool:
    """Check if cache key exists"""
    try:
        client = await get_redis()
        key = f"{settings.REDIS_PREFIX}{key}"
        return bool(await client.exists(key))
    except Exception as e:
        logger.error(f"Error checking cache: {e}")
        return False