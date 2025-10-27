"""
Districts API Router
"""

from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from ..database import get_db
from ..models import District, MGNREGASnapshot
from ..schemas import (
    DistrictList,
    DistrictListItem,
    StatesResponse,
    StateInfo,
    Snapshot,
    SnapshotBase,
    DashboardSnapshot,
    TrendData,
    TrendResponse,
    Comparison
)
from ..cache import get_cache, set_cache, delete_cache, clear_cache_pattern

router = APIRouter(prefix="/districts", tags=["districts"])


def _calculate_change(current: int, previous: int) -> Optional[float]:
    """
    Calculate percentage change between two values
    
    Returns:
        Percentage change rounded to 2 decimals, or None if previous is 0
    """
    if previous == 0:
        return None
    change = ((current - previous) / previous) * 100
    return round(change, 2)


@router.get("", response_model=DistrictList)
def get_districts(
    state: Optional[str] = Query(None, description="Filter by state name"),
    db: Session = Depends(get_db)
):
    """
    Get list of districts, optionally filtered by state
    """
    cache_key = f"districts:state:{state or 'all'}"
    
    # Try to get from cache
    cached = get_cache(cache_key)
    if cached:
        return DistrictList(**cached)
    
    # Query database
    query = db.query(District)
    if state:
        query = query.filter(func.lower(District.state) == func.lower(state))
    
    districts = query.order_by(District.district_name).all()
    
    # Format response
    district_items = [
        DistrictListItem(
            id=d.id,
            state=d.state,
            district_name=d.district_name,
            district_code=d.district_code
        ) for d in districts
    ]
    
    result = DistrictList(districts=district_items, total=len(district_items))
    
    # Cache the result
    set_cache(cache_key, result.model_dump(), ttl=3600)  # 1 hour
    
    return result


@router.get("/states", response_model=StatesResponse)
def get_states(db: Session = Depends(get_db)):
    """
    Get list of all states with district counts
    """
    cache_key = "states:all"
    
    # Try cache
    cached = get_cache(cache_key)
    if cached:
        return StatesResponse(**cached)
    
    # Query database
    results = db.query(
        District.state,
        func.count(District.id).label('count')
    ).group_by(District.state).order_by(District.state).all()
    
    states = [
        StateInfo(name=row[0], district_count=row[1])
        for row in results
    ]
    
    result = StatesResponse(states=states)
    
    # Cache for 1 hour
    set_cache(cache_key, result.model_dump(), ttl=3600)
    
    return result


@router.get("/{district_code}/snapshot", response_model=DashboardSnapshot)
def get_district_snapshot(
    district_code: str,
    db: Session = Depends(get_db)
):
    """
    Get latest snapshot for a district with comparison to previous month
    """
    cache_key = f"district:snapshot:{district_code}"
    
    # Try cache
    cached = get_cache(cache_key)
    if cached:
        return DashboardSnapshot(**cached)
    
    # Get district
    district = db.query(District).filter(District.district_code == district_code).first()
    if not district:
        raise HTTPException(status_code=404, detail=f"District '{district_code}' not found")
    
    # Get latest 2 snapshots
    snapshots = db.query(MGNREGASnapshot).filter(
        MGNREGASnapshot.district_id == district.id
    ).order_by(desc(MGNREGASnapshot.year), desc(MGNREGASnapshot.month)).limit(2).all()
    
    if not snapshots:
        raise HTTPException(status_code=404, detail=f"No data available for district '{district_code}'")
    
    current = SnapshotBase(
        year=snapshots[0].year,
        month=snapshots[0].month,
        people_benefited=snapshots[0].people_benefited,
        workdays_created=snapshots[0].workdays_created,
        wages_paid=snapshots[0].wages_paid,
        payments_on_time_percent=snapshots[0].payments_on_time_percent,
        works_completed=snapshots[0].works_completed
    )
    
    previous = None
    if len(snapshots) > 1:
        previous = SnapshotBase(
            year=snapshots[1].year,
            month=snapshots[1].month,
            people_benefited=snapshots[1].people_benefited,
            workdays_created=snapshots[1].workdays_created,
            wages_paid=snapshots[1].wages_paid,
            payments_on_time_percent=snapshots[1].payments_on_time_percent,
            works_completed=snapshots[1].works_completed
        )
    
    # Calculate comparisons
    comparison = {}
    if previous:
        comparison['people_benefited'] = _calculate_change(
            current.people_benefited, previous.people_benefited
        )
        comparison['workdays_created'] = _calculate_change(
            current.workdays_created, previous.workdays_created
        )
        comparison['wages_paid'] = _calculate_change(
            float(current.wages_paid), float(previous.wages_paid)
        )
        comparison['payments_on_time_percent'] = _calculate_change(
            float(current.payments_on_time_percent), float(previous.payments_on_time_percent)
        )
        comparison['works_completed'] = _calculate_change(
            current.works_completed, previous.works_completed
        )
    
    district_item = DistrictListItem(
        id=district.id,
        state=district.state,
        district_name=district.district_name,
        district_code=district.district_code
    )
    
    result = DashboardSnapshot(
        current=current,
        previous=previous,
        district=district_item,
        comparison=comparison
    )
    
    # Cache for 30 minutes
    set_cache(cache_key, result.model_dump(), ttl=1800)
    
    return result


@router.get("/{district_code}/trend", response_model=TrendResponse)
def get_district_trend(
    district_code: str,
    months: int = Query(6, ge=1, le=24, description="Number of months to retrieve"),
    db: Session = Depends(get_db)
):
    """
    Get trend data for a district (last N months)
    """
    cache_key = f"district:trend:{district_code}:{months}"
    
    # Try cache
    cached = get_cache(cache_key)
    if cached:
        return TrendResponse(**cached)
    
    # Get district
    district = db.query(District).filter(District.district_code == district_code).first()
    if not district:
        raise HTTPException(status_code=404, detail=f"District '{district_code}' not found")
    
    # Get snapshots
    snapshots = db.query(MGNREGASnapshot).filter(
        MGNREGASnapshot.district_id == district.id
    ).order_by(desc(MGNREGASnapshot.year), desc(MGNREGASnapshot.month)).limit(months).all()
    
    if not snapshots:
        raise HTTPException(status_code=404, detail=f"No trend data available for district '{district_code}'")
    
    # Format data for charts
    month_names = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]
    
    trends = []
    for snapshot in reversed(snapshots):  # Chronological order
        month_year = f"{month_names[snapshot.month - 1]} {snapshot.year}"
        trends.append(TrendData(
            month_year=month_year,
            people_benefited=snapshot.people_benefited,
            workdays_created=snapshot.workdays_created,
            wages_paid=snapshot.wages_paid,
            payments_on_time_percent=snapshot.payments_on_time_percent,
            works_completed=snapshot.works_completed
        ))
    
    district_item = DistrictListItem(
        id=district.id,
        state=district.state,
        district_name=district.district_name,
        district_code=district.district_code
    )
    
    result = TrendResponse(district=district_item, trends=trends)
    
    # Cache for 30 minutes
    set_cache(cache_key, result.model_dump(), ttl=1800)
    
    return result

