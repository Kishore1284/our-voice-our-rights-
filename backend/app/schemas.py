"""
Pydantic Schemas for Request/Response Validation
"""

from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Dict
from pydantic import BaseModel, Field


# ============================================================================
# District Schemas
# ============================================================================

class DistrictBase(BaseModel):
    """Base district schema"""
    state: str
    district_name: str
    district_code: str
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None


class District(DistrictBase):
    """Full district schema with ID"""
    id: int
    created_at: datetime
    
    model_config = {"from_attributes": True}


class DistrictListItem(BaseModel):
    """District item for list responses"""
    id: int
    state: str
    district_name: str
    district_code: str
    
    model_config = {"from_attributes": True}


class DistrictList(BaseModel):
    """List of districts with total count"""
    districts: List[DistrictListItem]
    total: int


# ============================================================================
# Snapshot Schemas
# ============================================================================

class SnapshotBase(BaseModel):
    """Base snapshot schema"""
    year: int
    month: int
    people_benefited: int = 0
    workdays_created: int = 0
    wages_paid: Decimal = Decimal("0.00")
    payments_on_time_percent: Decimal = Decimal("0.00")
    works_completed: int = 0


class Snapshot(SnapshotBase):
    """Full snapshot with IDs and metadata"""
    id: int
    district_id: int
    fetched_at: datetime
    
    model_config = {"from_attributes": True}


class SnapshotWithDistrict(SnapshotBase):
    """Snapshot with embedded district info"""
    district_name: str
    district_code: str
    state: str
    
    model_config = {"from_attributes": True}


# ============================================================================
# Dashboard & Analytics Schemas
# ============================================================================

class Comparison(BaseModel):
    """Percentage change comparison"""
    people_benefited: Optional[float] = None
    workdays_created: Optional[float] = None
    wages_paid: Optional[float] = None
    payments_on_time_percent: Optional[float] = None
    works_completed: Optional[float] = None


class DashboardSnapshot(BaseModel):
    """Current snapshot for dashboard"""
    current: SnapshotBase
    previous: Optional[SnapshotBase] = None
    district: DistrictListItem
    comparison: Dict[str, Optional[float]]


class TrendData(BaseModel):
    """Single trend data point for charts"""
    month_year: str  # Format: "Jan 2025"
    people_benefited: int
    workdays_created: int
    wages_paid: Decimal
    payments_on_time_percent: Decimal
    works_completed: int


class TrendResponse(BaseModel):
    """Trend data response"""
    district: DistrictListItem
    trends: List[TrendData]


# ============================================================================
# Geolocation Schemas
# ============================================================================

class GeolocateRequest(BaseModel):
    """Geolocation request"""
    latitude: float = Field(..., ge=-90, le=90, description="Latitude in decimal degrees")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude in decimal degrees")


class GeolocateResponse(BaseModel):
    """Geolocate response"""
    district: DistrictListItem
    distance_km: float
    
    
# ============================================================================
# API Response Schemas
# ============================================================================

class StateInfo(BaseModel):
    """State information with district count"""
    name: str
    district_count: int


class StatesResponse(BaseModel):
    """List of states response"""
    states: List[StateInfo]

