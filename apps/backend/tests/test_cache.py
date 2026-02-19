"""Tests for response caching."""

import pytest
from datetime import datetime, timedelta, UTC
from career_path.cache import ResponseCache


@pytest.fixture
def cache():
    """Create a fresh cache."""
    return ResponseCache(ttl_minutes=1)


def test_cache_set_and_get(cache):
    """Test basic cache set and get."""
    cache.set("test prompt", "test response")
    
    result = cache.get("test prompt")
    assert result == "test response"


def test_cache_miss(cache):
    """Test cache miss."""
    result = cache.get("nonexistent prompt")
    assert result is None


def test_cache_with_different_models(cache):
    """Test caching with different models."""
    cache.set("prompt", "response1", model="model1")
    cache.set("prompt", "response2", model="model2")
    
    assert cache.get("prompt", model="model1") == "response1"
    assert cache.get("prompt", model="model2") == "response2"


def test_cache_expiration(cache):
    """Test cache expiration."""
    cache.set("prompt", "response")
    
    # Manually expire by modifying timestamp
    key = cache._generate_key("prompt")
    cache._cache[key]["timestamp"] = datetime.now(UTC) - timedelta(minutes=2)
    
    result = cache.get("prompt")
    assert result is None
    assert key not in cache._cache  # Should be removed


def test_cache_hits_counter(cache):
    """Test hit counter increments."""
    cache.set("prompt", "response")
    
    cache.get("prompt")
    cache.get("prompt")
    cache.get("prompt")
    
    key = cache._generate_key("prompt")
    assert cache._cache[key]["hits"] == 3


def test_cache_clear(cache):
    """Test clearing cache."""
    cache.set("prompt1", "response1")
    cache.set("prompt2", "response2")
    
    cache.clear()
    
    assert cache.get("prompt1") is None
    assert cache.get("prompt2") is None
    assert len(cache._cache) == 0


def test_cache_stats_empty(cache):
    """Test stats for empty cache."""
    stats = cache.get_stats()
    
    assert stats["total_entries"] == 0
    assert stats["active_entries"] == 0
    assert stats["total_hits"] == 0
    assert stats["ttl_minutes"] == 1


def test_cache_stats_with_entries(cache):
    """Test stats with cached entries."""
    cache.set("prompt1", "response1")
    cache.set("prompt2", "response2")
    
    cache.get("prompt1")
    cache.get("prompt1")
    cache.get("prompt2")
    
    stats = cache.get_stats()
    
    assert stats["total_entries"] == 2
    assert stats["active_entries"] == 2
    assert stats["total_hits"] == 3


def test_cache_cleanup_expired(cache):
    """Test cleanup of expired entries."""
    cache.set("prompt1", "response1")
    cache.set("prompt2", "response2")
    cache.set("prompt3", "response3")
    
    # Expire two entries
    key1 = cache._generate_key("prompt1")
    key2 = cache._generate_key("prompt2")
    cache._cache[key1]["timestamp"] = datetime.now(UTC) - timedelta(minutes=2)
    cache._cache[key2]["timestamp"] = datetime.now(UTC) - timedelta(minutes=2)
    
    removed = cache.cleanup_expired()
    
    assert removed == 2
    assert len(cache._cache) == 1
    assert cache.get("prompt3") == "response3"


def test_cache_key_generation_consistency(cache):
    """Test that same prompt generates same key."""
    key1 = cache._generate_key("test prompt", "model1")
    key2 = cache._generate_key("test prompt", "model1")
    
    assert key1 == key2


def test_cache_key_generation_different_prompts(cache):
    """Test that different prompts generate different keys."""
    key1 = cache._generate_key("prompt1")
    key2 = cache._generate_key("prompt2")
    
    assert key1 != key2


def test_cache_key_generation_different_models(cache):
    """Test that different models generate different keys."""
    key1 = cache._generate_key("prompt", "model1")
    key2 = cache._generate_key("prompt", "model2")
    
    assert key1 != key2


def test_cache_ttl_custom(cache):
    """Test custom TTL."""
    custom_cache = ResponseCache(ttl_minutes=30)
    
    stats = custom_cache.get_stats()
    assert stats["ttl_minutes"] == 30


def test_cache_overwrite(cache):
    """Test overwriting cached value."""
    cache.set("prompt", "response1")
    cache.set("prompt", "response2")
    
    result = cache.get("prompt")
    assert result == "response2"


def test_cache_stats_with_expired(cache):
    """Test stats correctly count active vs total entries."""
    cache.set("prompt1", "response1")
    cache.set("prompt2", "response2")
    
    # Expire one entry
    key1 = cache._generate_key("prompt1")
    cache._cache[key1]["timestamp"] = datetime.now(UTC) - timedelta(minutes=2)
    
    stats = cache.get_stats()
    
    assert stats["total_entries"] == 2
    assert stats["active_entries"] == 1


def test_cache_multiple_operations(cache):
    """Test multiple cache operations."""
    # Set multiple entries
    for i in range(5):
        cache.set(f"prompt{i}", f"response{i}")
    
    # Get some entries
    cache.get("prompt0")
    cache.get("prompt1")
    cache.get("prompt1")
    
    # Check stats
    stats = cache.get_stats()
    assert stats["total_entries"] == 5
    assert stats["total_hits"] == 3
    
    # Clear and verify
    cache.clear()
    assert cache.get_stats()["total_entries"] == 0
