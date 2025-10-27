"""
Geolocation API Router
"""

import math
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..database import get_db
from ..models import District
from ..schemas import GeolocateRequest, GeolocateResponse, DistrictListItem

router = APIRouter(prefix="/geolocate", tags=["geolocate"])


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate distance between two points using Haversine formula
    
    Args:
        lat1, lon1: First point coordinates in decimal degrees
        lat2, lon2: Second point coordinates in decimal degrees
        
    Returns:
        Distance in kilometers
    """
    # Earth radius in kilometers
    R = 6371.0
    
    # Convert to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # Differences
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    distance = R * c
    return round(distance, 2)


@router.post("", response_model=GeolocateResponse)
def geolocate_district(
    request: GeolocateRequest,
    db: Session = Depends(get_db)
):
    """
    Find nearest district to given coordinates using Haversine formula
    """
    # Get all districts with coordinates
    districts = db.query(District).filter(
        District.latitude.isnot(None),
        District.longitude.isnot(None)
    ).all()
    
    if not districts:
        raise Exception("No districts with geographic data available")
    
    # Find nearest district
    nearest = None
    min_distance = float('inf')
    
    for district in districts:
        if district.latitude and district.longitude:
            distance = haversine_distance(
                request.latitude, request.longitude,
                float(district.latitude), float(district.longitude)
            )
            
            if distance < min_distance:
                min_distance = distance
                nearest = district
    
    if not nearest:
        raise Exception("Could not find nearest district")
    
    district_item = DistrictListItem(
        id=nearest.id,
        state=nearest.state,
        district_name=nearest.district_name,
        district_code=nearest.district_code
    )
    
    return GeolocateResponse(
        district=district_item,
        distance_km=min_distance
    )


@router.get("/test")
def geolocate_test(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    db: Session = Depends(get_db)
):
    """
    Test endpoint for geolocation (GET instead of POST)
    Useful for browser testing
    """
    request = GeolocateRequest(latitude=lat, longitude=lon)
    return geolocate_district(request, db)

