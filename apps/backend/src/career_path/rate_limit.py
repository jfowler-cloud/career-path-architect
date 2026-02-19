"""Rate limiting middleware."""

from datetime import datetime, timedelta, UTC
from typing import Dict, Tuple
from collections import defaultdict


class RateLimiter:
    """Simple in-memory rate limiter."""
    
    def __init__(self, requests_per_minute: int = 10, requests_per_hour: int = 100):
        """Initialize rate limiter.
        
        Args:
            requests_per_minute: Max requests per minute per IP
            requests_per_hour: Max requests per hour per IP
        """
        self._requests_per_minute = requests_per_minute
        self._requests_per_hour = requests_per_hour
        self._minute_requests: Dict[str, list] = defaultdict(list)
        self._hour_requests: Dict[str, list] = defaultdict(list)
    
    def _cleanup_old_requests(self, ip: str) -> None:
        """Remove old request timestamps.
        
        Args:
            ip: IP address
        """
        now = datetime.now(UTC)
        minute_ago = now - timedelta(minutes=1)
        hour_ago = now - timedelta(hours=1)
        
        # Clean minute requests
        self._minute_requests[ip] = [
            ts for ts in self._minute_requests[ip]
            if ts > minute_ago
        ]
        
        # Clean hour requests
        self._hour_requests[ip] = [
            ts for ts in self._hour_requests[ip]
            if ts > hour_ago
        ]
    
    def is_allowed(self, ip: str) -> Tuple[bool, str]:
        """Check if request is allowed.
        
        Args:
            ip: IP address
            
        Returns:
            Tuple of (is_allowed, reason)
        """
        self._cleanup_old_requests(ip)
        
        minute_count = len(self._minute_requests[ip])
        hour_count = len(self._hour_requests[ip])
        
        if minute_count >= self._requests_per_minute:
            return False, f"Rate limit exceeded: {self._requests_per_minute} requests per minute"
        
        if hour_count >= self._requests_per_hour:
            return False, f"Rate limit exceeded: {self._requests_per_hour} requests per hour"
        
        return True, ""
    
    def record_request(self, ip: str) -> None:
        """Record a request.
        
        Args:
            ip: IP address
        """
        now = datetime.now(UTC)
        self._minute_requests[ip].append(now)
        self._hour_requests[ip].append(now)
    
    def get_stats(self, ip: str) -> Dict:
        """Get rate limit stats for an IP.
        
        Args:
            ip: IP address
            
        Returns:
            Dictionary with stats
        """
        self._cleanup_old_requests(ip)
        
        minute_count = len(self._minute_requests[ip])
        hour_count = len(self._hour_requests[ip])
        
        return {
            "requests_last_minute": minute_count,
            "requests_last_hour": hour_count,
            "minute_limit": self._requests_per_minute,
            "hour_limit": self._requests_per_hour,
            "minute_remaining": max(0, self._requests_per_minute - minute_count),
            "hour_remaining": max(0, self._requests_per_hour - hour_count)
        }
    
    def reset(self, ip: str = None) -> None:
        """Reset rate limits.
        
        Args:
            ip: Optional IP to reset, or None for all
        """
        if ip:
            self._minute_requests.pop(ip, None)
            self._hour_requests.pop(ip, None)
        else:
            self._minute_requests.clear()
            self._hour_requests.clear()


# Global rate limiter instance
rate_limiter = RateLimiter(requests_per_minute=10, requests_per_hour=100)
