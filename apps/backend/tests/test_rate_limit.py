"""Tests for rate limiting."""

import pytest
from datetime import datetime, timedelta, UTC
from career_path.rate_limit import RateLimiter


@pytest.fixture
def limiter():
    """Create a fresh rate limiter."""
    return RateLimiter(requests_per_minute=5, requests_per_hour=20)


def test_rate_limiter_allows_first_request(limiter):
    """Test first request is allowed."""
    allowed, reason = limiter.is_allowed("192.168.1.1")
    assert allowed is True
    assert reason == ""


def test_rate_limiter_records_request(limiter):
    """Test recording requests."""
    limiter.record_request("192.168.1.1")
    stats = limiter.get_stats("192.168.1.1")
    assert stats["requests_last_minute"] == 1
    assert stats["requests_last_hour"] == 1


def test_rate_limiter_minute_limit(limiter):
    """Test minute rate limit."""
    ip = "192.168.1.1"
    
    # Make 5 requests (at limit)
    for _ in range(5):
        allowed, _ = limiter.is_allowed(ip)
        assert allowed is True
        limiter.record_request(ip)
    
    # 6th request should be blocked
    allowed, reason = limiter.is_allowed(ip)
    assert allowed is False
    assert "per minute" in reason


def test_rate_limiter_hour_limit(limiter):
    """Test hour rate limit."""
    ip = "192.168.1.1"
    
    # Simulate 20 requests over time (under minute limit)
    for i in range(20):
        # Manually add to hour requests
        limiter._hour_requests[ip].append(datetime.now(UTC))
    
    # Next request should be blocked by hour limit
    allowed, reason = limiter.is_allowed(ip)
    assert allowed is False
    assert "per hour" in reason


def test_rate_limiter_different_ips(limiter):
    """Test different IPs have separate limits."""
    limiter.record_request("192.168.1.1")
    limiter.record_request("192.168.1.2")
    
    stats1 = limiter.get_stats("192.168.1.1")
    stats2 = limiter.get_stats("192.168.1.2")
    
    assert stats1["requests_last_minute"] == 1
    assert stats2["requests_last_minute"] == 1


def test_rate_limiter_cleanup_old_requests(limiter):
    """Test cleanup of old requests."""
    ip = "192.168.1.1"
    
    # Add old request
    old_time = datetime.now(UTC) - timedelta(minutes=2)
    limiter._minute_requests[ip].append(old_time)
    
    # Cleanup should remove it
    limiter._cleanup_old_requests(ip)
    
    assert len(limiter._minute_requests[ip]) == 0


def test_rate_limiter_stats(limiter):
    """Test stats calculation."""
    ip = "192.168.1.1"
    
    limiter.record_request(ip)
    limiter.record_request(ip)
    
    stats = limiter.get_stats(ip)
    
    assert stats["requests_last_minute"] == 2
    assert stats["requests_last_hour"] == 2
    assert stats["minute_limit"] == 5
    assert stats["hour_limit"] == 20
    assert stats["minute_remaining"] == 3
    assert stats["hour_remaining"] == 18


def test_rate_limiter_reset_specific_ip(limiter):
    """Test resetting specific IP."""
    limiter.record_request("192.168.1.1")
    limiter.record_request("192.168.1.2")
    
    limiter.reset("192.168.1.1")
    
    stats1 = limiter.get_stats("192.168.1.1")
    stats2 = limiter.get_stats("192.168.1.2")
    
    assert stats1["requests_last_minute"] == 0
    assert stats2["requests_last_minute"] == 1


def test_rate_limiter_reset_all(limiter):
    """Test resetting all IPs."""
    limiter.record_request("192.168.1.1")
    limiter.record_request("192.168.1.2")
    
    limiter.reset()
    
    stats1 = limiter.get_stats("192.168.1.1")
    stats2 = limiter.get_stats("192.168.1.2")
    
    assert stats1["requests_last_minute"] == 0
    assert stats2["requests_last_minute"] == 0


def test_rate_limiter_remaining_counts(limiter):
    """Test remaining request counts."""
    ip = "192.168.1.1"
    
    for i in range(3):
        limiter.record_request(ip)
    
    stats = limiter.get_stats(ip)
    
    assert stats["minute_remaining"] == 2
    assert stats["hour_remaining"] == 17


def test_rate_limiter_zero_remaining(limiter):
    """Test zero remaining when at limit."""
    ip = "192.168.1.1"
    
    for i in range(5):
        limiter.record_request(ip)
    
    stats = limiter.get_stats(ip)
    
    assert stats["minute_remaining"] == 0


def test_rate_limiter_custom_limits():
    """Test custom rate limits."""
    custom_limiter = RateLimiter(requests_per_minute=2, requests_per_hour=10)
    
    stats = custom_limiter.get_stats("192.168.1.1")
    
    assert stats["minute_limit"] == 2
    assert stats["hour_limit"] == 10


def test_rate_limiter_multiple_requests_workflow(limiter):
    """Test realistic workflow with multiple requests."""
    ip = "192.168.1.1"
    
    # Make 3 requests
    for _ in range(3):
        allowed, _ = limiter.is_allowed(ip)
        assert allowed is True
        limiter.record_request(ip)
    
    # Check stats
    stats = limiter.get_stats(ip)
    assert stats["requests_last_minute"] == 3
    assert stats["minute_remaining"] == 2
    
    # Make 2 more (at limit)
    for _ in range(2):
        allowed, _ = limiter.is_allowed(ip)
        assert allowed is True
        limiter.record_request(ip)
    
    # Next should be blocked
    allowed, reason = limiter.is_allowed(ip)
    assert allowed is False
