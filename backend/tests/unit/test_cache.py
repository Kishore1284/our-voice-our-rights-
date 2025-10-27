"""
Unit tests for cache utilities
"""

import pytest
from app.cache import get_cache, set_cache, delete_cache
import json


class TestCacheFunctions:
    """Test cache utility functions"""
    
    def test_set_and_get_cache(self, mock_redis):
        """Test setting and getting cache values"""
        key = "test:key"
        value = {"test": "data", "count": 42}
        
        # Set cache
        result = set_cache(key, value, ttl=60)
        assert result is True
        
        # Get cache
        cached = get_cache(key)
        assert cached == value
    
    def test_get_cache_not_found(self, mock_redis):
        """Test getting non-existent cache key"""
        key = "test:nonexistent"
        
        cached = get_cache(key)
        assert cached is None
    
    def test_delete_cache(self, mock_redis):
        """Test deleting cache key"""
        key = "test:key"
        value = {"test": "data"}
        
        # Set and verify
        set_cache(key, value)
        assert get_cache(key) == value
        
        # Delete
        result = delete_cache(key)
        assert result is True
        
        # Verify deleted
        assert get_cache(key) is None
    
    def test_cache_with_complex_data(self, mock_redis):
        """Test cache with complex nested data"""
        key = "test:complex"
        value = {
            "nested": {
                "deep": {
                    "value": 123,
                    "list": [1, 2, 3],
                    "dict": {"a": 1, "b": 2}
                }
            }
        }
        
        set_cache(key, value)
        cached = get_cache(key)
        
        assert cached == value
        assert cached["nested"]["deep"]["value"] == 123
        assert cached["nested"]["deep"]["list"] == [1, 2, 3]
    
    def test_cache_ttl(self, mock_redis):
        """Test cache with TTL"""
        key = "test:ttl"
        value = {"test": "data"}
        
        result = set_cache(key, value, ttl=30)
        assert result is True
        
        cached = get_cache(key)
        assert cached == value

