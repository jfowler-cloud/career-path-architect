"""Simple caching for LLM responses."""

import hashlib
import json
from typing import Optional, Dict, Any
from datetime import datetime, timedelta, UTC


class ResponseCache:
    """In-memory cache for LLM responses."""
    
    def __init__(self, ttl_minutes: int = 60):
        """Initialize cache with TTL.
        
        Args:
            ttl_minutes: Time to live in minutes
        """
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._ttl = timedelta(minutes=ttl_minutes)
    
    def _generate_key(self, prompt: str, model: str = "default") -> str:
        """Generate cache key from prompt and model."""
        content = f"{model}:{prompt}"
        return hashlib.sha256(content.encode()).hexdigest()
    
    def get(self, prompt: str, model: str = "default") -> Optional[str]:
        """Get cached response if available and not expired.
        
        Args:
            prompt: The prompt text
            model: Model identifier
            
        Returns:
            Cached response or None
        """
        key = self._generate_key(prompt, model)
        
        if key not in self._cache:
            return None
        
        entry = self._cache[key]
        
        # Check if expired
        if datetime.now(UTC) - entry["timestamp"] > self._ttl:
            del self._cache[key]
            return None
        
        entry["hits"] += 1
        return entry["response"]
    
    def set(self, prompt: str, response: str, model: str = "default") -> None:
        """Cache a response.
        
        Args:
            prompt: The prompt text
            response: The response to cache
            model: Model identifier
        """
        key = self._generate_key(prompt, model)
        self._cache[key] = {
            "response": response,
            "timestamp": datetime.now(UTC),
            "hits": 0
        }
    
    def clear(self) -> None:
        """Clear all cached entries."""
        self._cache.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics.
        
        Returns:
            Dictionary with cache stats
        """
        now = datetime.now(UTC)
        active_entries = sum(
            1 for entry in self._cache.values()
            if now - entry["timestamp"] <= self._ttl
        )
        
        total_hits = sum(entry["hits"] for entry in self._cache.values())
        
        return {
            "total_entries": len(self._cache),
            "active_entries": active_entries,
            "total_hits": total_hits,
            "ttl_minutes": self._ttl.total_seconds() / 60
        }
    
    def cleanup_expired(self) -> int:
        """Remove expired entries.
        
        Returns:
            Number of entries removed
        """
        now = datetime.now(UTC)
        expired_keys = [
            key for key, entry in self._cache.items()
            if now - entry["timestamp"] > self._ttl
        ]
        
        for key in expired_keys:
            del self._cache[key]
        
        return len(expired_keys)


# Global cache instance
response_cache = ResponseCache(ttl_minutes=60)
