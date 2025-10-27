"""
Unit tests for Pydantic schemas
"""

import pytest
from datetime import datetime
from decimal import Decimal
from app.schemas import (
    District,
    DistrictListItem,
    SnapshotBase,
    DashboardSnapshot,
    TrendData,
    GeolocateRequest
)


class TestDistrictSchemas:
    """Test district-related schemas"""
    
    def test_district_list_item_creation(self):
        """Test creating DistrictListItem"""
        data = {
            "id": 1,
            "state": "Uttar Pradesh",
            "district_name": "Lucknow",
            "district_code": "UP-LUC"
        }
        
        item = DistrictListItem(**data)
        
        assert item.id == 1
        assert item.state == "Uttar Pradesh"
        assert item.district_name == "Lucknow"
        assert item.district_code == "UP-LUC"
    
    def test_district_schema(self):
        """Test District schema with datetime"""
        data = {
            "id": 1,
            "state": "Uttar Pradesh",
            "district_name": "Lucknow",
            "district_code": "UP-LUC",
            "latitude": Decimal("26.8467"),
            "longitude": Decimal("80.9462"),
            "created_at": datetime.now()
        }
        
        district = District(**data)
        
        assert district.id == 1
        assert district.district_code == "UP-LUC"


class TestSnapshotSchemas:
    """Test snapshot-related schemas"""
    
    def test_snapshot_base_creation(self):
        """Test creating SnapshotBase"""
        data = {
            "year": 2025,
            "month": 1,
            "people_benefited": 45000,
            "workdays_created": 900000,
            "wages_paid": Decimal("158400000.00"),
            "payments_on_time_percent": Decimal("92.5"),
            "works_completed": 350
        }
        
        snapshot = SnapshotBase(**data)
        
        assert snapshot.year == 2025
        assert snapshot.people_benefited == 45000
        assert snapshot.wages_paid == Decimal("158400000.00")
    
    def test_trend_data_creation(self):
        """Test creating TrendData"""
        data = {
            "month_year": "Jan 2025",
            "people_benefited": 45000,
            "workdays_created": 900000,
            "wages_paid": Decimal("158400000.00"),
            "payments_on_time_percent": Decimal("92.5"),
            "works_completed": 350
        }
        
        trend = TrendData(**data)
        
        assert trend.month_year == "Jan 2025"
        assert trend.people_benefited == 45000


class TestGeolocationSchemas:
    """Test geolocation schemas"""
    
    def test_geolocate_request_creation(self):
        """Test creating GeolocateRequest"""
        data = {
            "latitude": 26.8467,
            "longitude": 80.9462
        }
        
        request = GeolocateRequest(**data)
        
        assert request.latitude == 26.8467
        assert request.longitude == 80.9462
    
    def test_geolocate_request_validation(self):
        """Test GeolocateRequest field validation"""
        with pytest.raises(Exception):
            # Invalid latitude (out of range)
            GeolocateRequest(latitude=100, longitude=80.9462)
        
        with pytest.raises(Exception):
            # Invalid longitude (out of range)
            GeolocateRequest(latitude=26.8467, longitude=200)


class TestDashboardSnapshot:
    """Test DashboardSnapshot schema"""
    
    def test_dashboard_snapshot_creation(self):
        """Test creating DashboardSnapshot"""
        data = {
            "current": {
                "year": 2025,
                "month": 1,
                "people_benefited": 45000,
                "workdays_created": 900000,
                "wages_paid": Decimal("158400000.00"),
                "payments_on_time_percent": Decimal("92.5"),
                "works_completed": 350
            },
            "previous": {
                "year": 2024,
                "month": 12,
                "people_benefited": 44000,
                "workdays_created": 880000,
                "wages_paid": Decimal("154880000.00"),
                "payments_on_time_percent": Decimal("91.0"),
                "works_completed": 340
            },
            "district": {
                "id": 1,
                "state": "Uttar Pradesh",
                "district_name": "Lucknow",
                "district_code": "UP-LUC"
            },
            "comparison": {
                "people_benefited": 2.27,
                "workdays_created": 2.27,
                "wages_paid": 2.27,
                "payments_on_time_percent": 1.65,
                "works_completed": 2.94
            }
        }
        
        dashboard = DashboardSnapshot(**data)
        
        assert dashboard.current.year == 2025
        assert dashboard.previous is not None
        assert dashboard.district.district_code == "UP-LUC"
        assert dashboard.comparison["people_benefited"] == 2.27

