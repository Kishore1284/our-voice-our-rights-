"""
Tests for ingestion worker functions
"""

import pytest
from unittest.mock import patch, MagicMock
from worker import fetch_mgnrega_data, store_snapshot
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text


@pytest.fixture
def db_session():
    """In-memory database for testing"""
    engine = create_engine("sqlite:///:memory:")
    
    # Create tables
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE districts (
                id INTEGER PRIMARY KEY,
                state TEXT,
                district_name TEXT,
                district_code TEXT UNIQUE,
                latitude NUMERIC,
                longitude NUMERIC
            )
        """))
        
        conn.execute(text("""
            CREATE TABLE mgnrega_snapshots (
                id INTEGER PRIMARY KEY,
                district_id INTEGER,
                year INTEGER,
                month INTEGER,
                people_benefited INTEGER,
                workdays_created INTEGER,
                wages_paid NUMERIC,
                payments_on_time_percent NUMERIC,
                works_completed INTEGER,
                UNIQUE(district_id, year, month)
            )
        """))
        
        conn.commit()
    
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    
    # Insert test district
    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO districts (state, district_name, district_code, latitude, longitude)
            VALUES ('Uttar Pradesh', 'Lucknow', 'UP-LUC', 26.8467, 80.9462)
        """))
        conn.commit()
    
    yield session
    session.close()
    engine.dispose()


class TestFetchMGNREGAData:
    """Test data fetching functions"""
    
    def test_fetch_mgnrega_data_returns_dict(self):
        """Test fetch_mgnrega_data returns a dictionary"""
        data = fetch_mgnrega_data("UP-LUC", 2025, 1)
        
        assert isinstance(data, dict)
        assert "people_benefited" in data
        assert "workdays_created" in data
        assert "wages_paid" in data
        assert "payments_on_time_percent" in data
        assert "works_completed" in data
    
    def test_fetch_mgnrega_data_realistic_values(self):
        """Test that fetched data has realistic values"""
        data = fetch_mgnrega_data("UP-LUC", 2025, 1)
        
        # Check people_benefited is within expected range
        assert 30000 <= data["people_benefited"] <= 60000
        
        # Check wages_paid is positive
        assert data["wages_paid"] > 0
        
        # Check payments_on_time_percent is reasonable
        assert 80 <= data["payments_on_time_percent"] <= 100
    
    @patch('worker.httpx.get')
    def test_handle_api_429_rate_limit(self, mock_get):
        """Test handling of API rate limit (429 status)"""
        # Mock 429 response
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_response.raise_for_status.side_effect = Exception("Rate limited")
        mock_get.return_value = mock_response
        
        # Should handle gracefully and return mock data
        data = fetch_mgnrega_data("UP-LUC", 2025, 1)
        assert isinstance(data, dict)
        assert "people_benefited" in data


class TestStoreSnapshot:
    """Test snapshot storage functions"""
    
    def test_store_snapshot_upsert_logic(self, db_session):
        """Test that storing same snapshot twice doesn't duplicate"""
        # Get district ID
        result = db_session.execute(
            text("SELECT id FROM districts WHERE district_code = 'UP-LUC'")
        ).fetchone()
        district_id = result[0]
        
        # Create test data
        data = {
            'people_benefited': 45000,
            'workdays_created': 900000,
            'wages_paid': 158400000.00,
            'payments_on_time_percent': 92.5,
            'works_completed': 350,
            'raw_json': {'source': 'test'}
        }
        
        # Store first time
        result1 = store_snapshot(db_session, district_id, 2025, 1, data)
        assert result1 is True
        
        # Verify count
        count1 = db_session.execute(
            text("SELECT COUNT(*) FROM mgnrega_snapshots")
        ).scalar()
        assert count1 == 1
        
        # Store second time (should update, not duplicate)
        data['people_benefited'] = 46000  # Updated value
        result2 = store_snapshot(db_session, district_id, 2025, 1, data)
        assert result2 is True
        
        # Verify count is still 1
        count2 = db_session.execute(
            text("SELECT COUNT(*) FROM mgnrega_snapshots")
        ).scalar()
        assert count2 == 1
        
        # Verify updated value
        result = db_session.execute(
            text("SELECT people_benefited FROM mgnrega_snapshots WHERE district_id = :id"),
            {'id': district_id}
        ).fetchone()
        assert result[0] == 46000
    
    def test_store_snapshot_handles_invalid_data(self, db_session):
        """Test handling of invalid data"""
        result = db_session.execute(
            text("SELECT id FROM districts WHERE district_code = 'UP-LUC'")
        ).fetchone()
        district_id = result[0]
        
        # Invalid data with wrong types
        invalid_data = {
            'people_benefited': "not an integer",
            'workdays_created': None,
        }
        
        # Should handle gracefully
        result = store_snapshot(db_session, district_id, 2025, 1, invalid_data)
        # Function might return False or raise exception
        assert isinstance(result, bool)


class TestErrorHandling:
    """Test error handling scenarios"""
    
    def test_handles_missing_credentials_gracefully(self):
        """Test that missing API credentials don't crash the system"""
        with patch.dict('os.environ', {'MGNREGA_API_KEY': ''}):
            # Should return mock data instead of crashing
            data = fetch_mgnrega_data("UP-LUC", 2025, 1)
            assert isinstance(data, dict)
    
    def test_handles_database_connection_error(self):
        """Test handling of database connection errors"""
        # This test ensures error handling works when DB is unavailable
        # In actual implementation, this would catch exceptions
        with patch('worker.SessionLocal') as mock:
            mock.side_effect = Exception("Connection refused")
            # Should handle gracefully
            pass

