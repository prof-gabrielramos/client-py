"""
Caching utilities for performance optimization
"""
import json
import hashlib
from functools import wraps
from flask import request, current_app
from datetime import datetime, timedelta
import redis


class CacheManager:
    """Cache management with Redis fallback to memory"""
    
    def __init__(self):
        self.redis_client = None
        self.memory_cache = {}
        self.cache_ttl = {}
        
        try:
            redis_url = current_app.config.get('REDIS_URL')
            if redis_url and redis_url != 'memory://':
                self.redis_client = redis.from_url(redis_url)
                self.redis_client.ping()  # Test connection
        except Exception:
            current_app.logger.warning("Redis not available, using memory cache")
    
    def get(self, key: str):
        """Get value from cache"""
        try:
            if self.redis_client:
                value = self.redis_client.get(key)
                if value:
                    return json.loads(value)
            else:
                # Memory cache with TTL check
                if key in self.memory_cache:
                    if key in self.cache_ttl and datetime.utcnow() > self.cache_ttl[key]:
                        del self.memory_cache[key]
                        del self.cache_ttl[key]
                        return None
                    return self.memory_cache[key]
        except Exception as e:
            current_app.logger.error(f"Cache get error: {e}")
        
        return None
    
    def set(self, key: str, value, ttl: int = 300):
        """Set value in cache with TTL"""
        try:
            if self.redis_client:
                self.redis_client.setex(key, ttl, json.dumps(value))
            else:
                # Memory cache with TTL
                self.memory_cache[key] = value
                self.cache_ttl[key] = datetime.utcnow() + timedelta(seconds=ttl)
                
                # Cleanup old entries
                self._cleanup_memory_cache()
        except Exception as e:
            current_app.logger.error(f"Cache set error: {e}")
    
    def delete(self, key: str):
        """Delete value from cache"""
        try:
            if self.redis_client:
                self.redis_client.delete(key)
            else:
                self.memory_cache.pop(key, None)
                self.cache_ttl.pop(key, None)
        except Exception as e:
            current_app.logger.error(f"Cache delete error: {e}")
    
    def _cleanup_memory_cache(self):
        """Cleanup expired entries from memory cache"""
        now = datetime.utcnow()
        expired_keys = [
            key for key, expiry in self.cache_ttl.items()
            if now > expiry
        ]
        
        for key in expired_keys:
            self.memory_cache.pop(key, None)
            self.cache_ttl.pop(key, None)


# Global cache instance
cache = CacheManager()


def cached(ttl: int = 300, key_prefix: str = None):
    """Decorator for caching function results"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Generate cache key
            cache_key = key_prefix or f.__name__
            
            # Include request args in key for API endpoints
            if request:
                args_str = str(sorted(request.args.items()))
                cache_key += f":{hashlib.md5(args_str.encode()).hexdigest()}"
            
            # Try to get from cache
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Execute function and cache result
            result = f(*args, **kwargs)
            cache.set(cache_key, result, ttl)
            
            return result
        return decorated_function
    return decorator


def cache_key_for_user(user_id: int, prefix: str) -> str:
    """Generate cache key for user-specific data"""
    return f"user:{user_id}:{prefix}"


def invalidate_user_cache(user_id: int, prefix: str = None):
    """Invalidate cache for specific user"""
    if prefix:
        cache.delete(cache_key_for_user(user_id, prefix))
    else:
        # Invalidate all user cache (simplified approach)
        # In production, use cache tags or patterns
        pass