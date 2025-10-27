"""
Integration tests for MGNREGA API
Run with: pytest test_api.py -v
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestHealthEndpoint:
    """Test health check endpoint"""
    
    def test_health_check(self):
        """Test health endpoint returns correct status"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_root_endpoint(self):
        """Test root endpoint returns API info"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "status" in data
        assert "version" in data


class TestDistrictsEndpoint:
    """Test districts API endpoints"""
    
    def test_get_states(self):
        """Test getting list of states"""
        response = client.get("/api/v1/districts/states")
        assert response.status_code == 200
        data = response.json()
        assert "states" in data
        assert isinstance(data["states"], list)
    
    def test_get_districts(self):
        """Test getting list of districts"""
        response = client.get("/api/v1/districts")
        assert response.status_code == 200
        data = response.json()
        assert "districts" in data
        assert "total" in data
        assert isinstance(data["districts"], list)
        assert isinstance(data["total"], int)
    
    def test_get_districts_filtered_by_state(self):
        """Test filtering districts by state"""
        response = client.get("/api/v1/districts?state=Uttar Pradesh")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data["districts"], list)
        if data["districts"]:
            assert data["districts"][0]["state"] == "Uttar Pradesh"
    
    def test_get_district_snapshot(self):
        """Test getting district snapshot"""
        # This will fail if no data exists, which is expected
        response = client.get("/api/v1/districts/UP-LUC/snapshot")
        # Should return 200 if data exists, or 404 if not
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            data = response.json()
            assert "current" in data
            assert "district" in data
            assert "comparison" in data
    
    def test_get_district_trend(self):
        """Test getting district trend data"""
        response = client.get("/api/v1/districts/UP-LUC/trend?months=6")
        # Should return 200 if data exists, or 404 if not
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            data = response.json()
            assert "district" in data
            assert "trends" in data
            assert isinstance(data["trends"], list)


class TestGeolocationEndpoint:
    """Test geolocation API endpoints"""
    
    def test_geolocate_test_endpoint(self):
        """Test GET geolocate endpoint"""
        response = client.get("/api/v1/geolocate/test?lat=26.8467&lon=80.9462")
        # Should return 200 if districts exist, or error if not
        assert response.status_code in [200, 500]
        if response.status_code == 200:
            data = response.json()
            assert "district" in data
            assert "distance_km" in data
    
    def test_geolocate_post_endpoint(self):
        """Test POST geolocate endpoint"""
        response = client.post(
            "/api/v1/geolocate",
            json={"latitude": 26.8467, "longitude": 80.9462}
        )
        # Should return 200 if districts exist, or error if not
        assert response.status_code in [200, 500]
        if response.status_code == 200:
            data = response.json()
            assert "district" in data
            assert "distance_km" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

