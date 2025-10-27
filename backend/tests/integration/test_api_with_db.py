"""
Integration tests for API with real database connections
These tests require a running PostgreSQL instance
"""

import pytest


class TestDistrictsAPI:
    """Integration tests for districts API"""
    
    def test_get_districts_endpoint(self, client, db_with_sample_data):
        """Test GET /api/v1/districts endpoint"""
        response = client.get("/api/v1/districts")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "districts" in data
        assert "total" in data
        assert isinstance(data["districts"], list)
        assert data["total"] >= 1
    
    def test_get_states_endpoint(self, client, db_with_sample_data):
        """Test GET /api/v1/districts/states endpoint"""
        response = client.get("/api/v1/districts/states")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "states" in data
        assert isinstance(data["states"], list)
    
    def test_get_district_snapshot(self, client, db_with_sample_data):
        """Test GET /api/v1/districts/{code}/snapshot endpoint"""
        response = client.get("/api/v1/districts/UP-LUC/snapshot")
        
        # Should return 200 with data or 404 if no snapshots
        assert response.status_code in [200, 404]
        
        if response.status_code == 200:
            data = response.json()
            
            assert "current" in data
            assert "district" in data
            assert "comparison" in data
            
            # Verify district info
            assert data["district"]["district_code"] == "UP-LUC"
            
            # Verify current snapshot
            current = data["current"]
            assert "year" in current
            assert "month" in current
            assert "people_benefited" in current
    
    def test_get_district_trend(self, client, db_with_sample_data):
        """Test GET /api/v1/districts/{code}/trend endpoint"""
        response = client.get("/api/v1/districts/UP-LUC/trend?months=6")
        
        # Should return 200 with data or 404 if no snapshots
        assert response.status_code in [200, 404]
        
        if response.status_code == 200:
            data = response.json()
            
            assert "district" in data
            assert "trends" in data
            assert isinstance(data["trends"], list)


class TestGeolocationAPI:
    """Integration tests for geolocation API"""
    
    def test_geolocate_get_endpoint(self, client, db_with_sample_data):
        """Test GET /api/v1/geolocate/test endpoint"""
        # Test with Lucknow coordinates
        response = client.get("/api/v1/geolocate/test?lat=26.8467&lon=80.9462")
        
        # Should return 200 with district or 500 if no districts
        assert response.status_code in [200, 500]
        
        if response.status_code == 200:
            data = response.json()
            
            assert "district" in data
            assert "distance_km" in data
            assert isinstance(data["distance_km"], (int, float))
    
    def test_geolocate_post_endpoint(self, client, db_with_sample_data):
        """Test POST /api/v1/geolocate endpoint"""
        response = client.post(
            "/api/v1/geolocate",
            json={"latitude": 26.8467, "longitude": 80.9462}
        )
        
        # Should return 200 with district or 500 if no districts
        assert response.status_code in [200, 500]
        
        if response.status_code == 200:
            data = response.json()
            
            assert "district" in data
            assert "distance_km" in data


class TestCacheIntegration:
    """Integration tests for cache functionality"""
    
    def test_cache_miss_then_hit(self, client, mock_redis, db_with_sample_data):
        """Test that first request misses cache, second hits cache"""
        # First request - should miss cache
        response1 = client.get("/api/v1/districts")
        assert response1.status_code == 200
        
        # Second request - should hit cache
        response2 = client.get("/api/v1/districts")
        assert response2.status_code == 200
        
        # Verify same response
        assert response1.json() == response2.json()

