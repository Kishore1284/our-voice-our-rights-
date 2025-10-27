"""
Redis Cache Utilities
"""

import json
import logging
from typing import Any, Optional
from redis import Redis

from .config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# Initialize Redis client
try:
    redis_client = Redis.from_url(settings.redis_url, decode_responses=False)
except Exception as e:
    logger.error(f"Failed to connect to Redis: {e}")
    redis_client = None


def get_cache(key: str) -> Optional[Any]:
    """
    Retrieve value from Redis cache
    
    Args:
        key: Cache key
        
    Returns:
        Deserialized value or None if not found
    """
    if not redis_client:
        return None
    
    try:
        data = redis_client.get(key)
        if data:
            return json.loads(data)
    except Exception as e:
        logger.error(f"Cache get error for key {key}: {e}")
    
    return None


def set_cache(key: str, value: Any, ttl: int = None) -> bool:
    """
    Store value in Redis cache
    
    Args:
        key: Cache key
        value: Value to cache (will be JSON serialized)
        ttl: Time to live in seconds (defaults to settings.cache_ttl)
        
    Returns:
        True if successful, False otherwise
    """
    if not redis_client:
        return False
    
    try:
        serialized = json.dumps(value, default=str)
        ttl = ttl or settings.cache_ttl
        redis_client.setex(key, ttl, serialized)
        return True
    except Exception as e:
        logger.error(f"Cache set error for key {key}: {e}")
        return False


def delete_cache(key: str) -> bool:
    """
    Delete key from Redis cache
    
    Args:
        key: Cache key to delete
        
    Returns:
        True if deleted, False otherwise
    """
    if not redis_client:
        return False
    
    try:
        redis_client.delete(key)
        return True
    except Exception as e:
        logger.error(f"Cache delete error for key {key}: {e}")
        return False


def clear_cache_pattern(pattern: str) -> int:
    """
    Clear all keys matching a pattern
    
    Args:
        pattern: Redis key pattern (e.g., "district:*")
        
    Returns:
        Number of keys deleted
    """
    if not redis_client:
        return 0
    
    try:
        keys = redis_client.keys(pattern)
        if keys:
            return redis_client.delete(*keys)
        return 0
    except Exception as e:
        logger.error(f"Cache clear pattern error for {pattern}: {e}")
        return 0

