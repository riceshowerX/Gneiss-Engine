"""
Advanced caching utilities for Gneiss Engine.
"""

import asyncio
import hashlib
import pickle
from functools import wraps
from typing import Any, Callable, Optional, TypeVar

import redis.asyncio as redis
from loguru import logger

T = TypeVar("T")

# Global Redis connection pool
_redis_pool: Optional[redis.Redis] = None

def get_redis() -> redis.Redis:
    """Get Redis connection with connection pooling."""
    global _redis_pool
    if _redis_pool is None:
        _redis_pool = redis.Redis.from_url(
            "redis://localhost:6379/0",
            encoding="utf-8",
            decode_responses=False,
            max_connections=20,
        )
    return _redis_pool

async def async_lru_cache(maxsize: int = 128):
    """Async LRU cache decorator with Redis backend."""
    def decorator(func: Callable[..., Any]):
        cache = {}
        keys = []
        
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key
            key_data = pickle.dumps((args, kwargs))
            key_hash = hashlib.md5(key_data).hexdigest()
            
            # Try to get from memory cache first
            if key_hash in cache:
                keys.remove(key_hash)
                keys.append(key_hash)
                return cache[key_hash]
            
            # Try to get from Redis
            redis_client = get_redis()
            try:
                cached = await redis_client.get(f"cache:{func.__name__}:{key_hash}")
                if cached:
                    result = pickle.loads(cached)
                    cache[key_hash] = result
                    keys.append(key_hash)
                    
                    # Enforce maxsize
                    if len(keys) > maxsize:
                        old_key = keys.pop(0)
                        cache.pop(old_key, None)
                    
                    return result
            except Exception as e:
                logger.warning(f"Redis cache failed: {e}")
            
            # Call function if not cached
            result = await func(*args, **kwargs)
            
            # Store in memory cache
            cache[key_hash] = result
            keys.append(key_hash)
            
            # Enforce maxsize
            if len(keys) > maxsize:
                old_key = keys.pop(0)
                cache.pop(old_key, None)
            
            # Store in Redis async
            try:
                redis_client = get_redis()
                await redis_client.setex(
                    f"cache:{func.__name__}:{key_hash}",
                    3600,  # 1 hour TTL
                    pickle.dumps(result)
                )
            except Exception as e:
                logger.warning(f"Redis cache set failed: {e}")
            
            return result
        
        return wrapper
    
    return decorator

class DistributedLock:
    """Distributed lock using Redis."""
    
    def __init__(self, name: str, timeout: int = 30):
        self.name = f"lock:{name}"
        self.timeout = timeout
        self.redis = get_redis()
    
    async def acquire(self) -> bool:
        """Acquire distributed lock."""
        try:
            return await self.redis.set(
                self.name, "locked", nx=True, ex=self.timeout
            )
        except Exception:
            return False
    
    async def release(self):
        """Release distributed lock."""
        try:
            await self.redis.delete(self.name)
        except Exception:
            pass
    
    async def __aenter__(self):
        acquired = await self.acquire()
        if not acquired:
            raise Exception(f"Could not acquire lock {self.name}")
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.release()

def cache_result(ttl: int = 300, key_func: Optional[Callable] = None):
    """Generic result caching decorator."""
    def decorator(func: Callable[..., Any]):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                key_data = pickle.dumps((args, kwargs))
                cache_key = hashlib.md5(key_data).hexdigest()
            
            full_key = f"result:{func.__module__}:{func.__name__}:{cache_key}"
            
            # Try Redis first
            redis_client = get_redis()
            try:
                cached = await redis_client.get(full_key)
                if cached:
                    return pickle.loads(cached)
            except Exception:
                pass
            
            # Execute function
            result = await func(*args, **kwargs)
            
            # Cache result
            try:
                await redis_client.setex(full_key, ttl, pickle.dumps(result))
            except Exception:
                pass
            
            return result
        
        return wrapper
    
    return decorator

async def clear_cache(pattern: str = "*"):
    """Clear cache entries matching pattern."""
    redis_client = get_redis()
    try:
        keys = await redis_client.keys(pattern)
        if keys:
            await redis_client.delete(*keys)
    except Exception as e:
        logger.error(f"Cache clearance failed: {e}")

async def get_cache_stats() -> Dict[str, Any]:
    """Get cache statistics."""
    redis_client = get_redis()
    try:
        info = await redis_client.info("memory")
        return {
            "used_memory": info.get("used_memory", 0),
            "max_memory": info.get("maxmemory", 0),
            "key_count": await redis_client.dbsize(),
        }
    except Exception:
        return {"error": "Could not retrieve cache stats"}