"""
Unit tests for health endpoint
"""

import pytest


class TestHealthEndpoint:
    """Test health check endpoint"""
    
    def test_health_check_returns_ok(self, client):
        """Test health endpoint returns status: ok"""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert isinstance(data, dict)
    
    def test_health_check_response_structure(self, client):
        """Test health endpoint response structure"""
        response = client.get("/health")
        data = response.json()
        
        assert "status" in data
        assert len(data) == 1
    
    def test_health_check_with_real_client(self, client):
        """Test health endpoint with full client"""
        response = client.get("/health", headers={"Accept": "application/json"})
        
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"
        data = response.json()
        assert data["status"] == "ok"

