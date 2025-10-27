"""
Pytest configuration and shared fixtures
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import fakeredis
import json

from app.database import Base, get_db
from app.cache import redis_client
from app.main import app


# ============================================================================
# Database Fixtures
# ============================================================================

@pytest.fixture(scope="function")
def db_session():
    """In-memory SQLite database for unit tests"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session):
    """FastAPI test client with overridden database"""
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


# ============================================================================
# Redis Mock Fixture
# ============================================================================

@pytest.fixture(scope="function")
def mock_redis(monkeypatch):
    """Mock Redis client using fakeredis"""
    fake_redis = fakeredis.FakeStrictRedis()
    
    # Monkeypatch the redis client
    monkeypatch.setattr('app.cache.redis_client', fake_redis)
    
    yield fake_redis
    
    fake_redis.flushall()


# ============================================================================
# Sample Data Fixtures
# ============================================================================

@pytest.fixture
def sample_district_data():
    """Sample district data for testing"""
    return {
        "state": "Uttar Pradesh",
        "district_name": "Lucknow",
        "district_code": "UP-LUC",
        "latitude": 26.8467,
        "longitude": 80.9462
    }


@pytest.fixture
def sample_snapshot_data():
    """Sample snapshot data for testing"""
    return {
        "year": 2025,
        "month": 1,
        "people_benefited": 45000,
        "workdays_created": 900000,
        "wages_paid": 158400000.00,
        "payments_on_time_percent": 92.5,
        "works_completed": 350
    }


@pytest.fixture
def db_with_sample_data(db_session, sample_district_data, sample_snapshot_data):
    """Database populated with sample data"""
    # Insert district
    db_session.execute(
        """
        INSERT INTO districts (state, district_name, district_code, latitude, longitude)
        VALUES (:state, :name, :code, :lat, :lon)
        """,
        {
            "state": sample_district_data["state"],
            "name": sample_district_data["district_name"],
            "code": sample_district_data["district_code"],
            "lat": sample_district_data["latitude"],
            "lon": sample_district_data["longitude"]
        }
    )
    db_session.commit()
    
    # Get district ID
    result = db_session.execute(
        "SELECT id FROM districts WHERE district_code = :code",
        {"code": sample_district_data["district_code"]}
    )
    district_id = result.scalar()
    
    # Insert snapshot
    db_session.execute(
        """
        INSERT INTO mgnrega_snapshots
        (district_id, year, month, people_benefited, workdays_created,
         wages_paid, payments_on_time_percent, works_completed)
        VALUES (:district_id, :year, :month, :people, :workdays,
                :wages, :payments, :works)
        """,
        {
            "district_id": district_id,
            "year": sample_snapshot_data["year"],
            "month": sample_snapshot_data["month"],
            "people": sample_snapshot_data["people_benefited"],
            "workdays": sample_snapshot_data["workdays_created"],
            "wages": sample_snapshot_data["wages_paid"],
            "payments": sample_snapshot_data["payments_on_time_percent"],
            "works": sample_snapshot_data["works_completed"]
        }
    )
    db_session.commit()
    
    yield db_session

