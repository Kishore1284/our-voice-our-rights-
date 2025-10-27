"""
Unit tests for database utilities
"""

import pytest


class TestDatabaseOperations:
    """Test database utility functions"""
    
    def test_get_db_yields_session(self, db_session):
        """Test database session factory yields session"""
        assert db_session is not None
        assert hasattr(db_session, 'execute')
    
    def test_insert_district(self, db_session, sample_district_data):
        """Test inserting a district into database"""
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
        
        # Verify insertion
        result = db_session.execute(
            "SELECT district_code, district_name FROM districts WHERE district_code = :code",
            {"code": sample_district_data["district_code"]}
        ).fetchone()
        
        assert result is not None
        assert result[0] == sample_district_data["district_code"]
        assert result[1] == sample_district_data["district_name"]
    
    def test_upsert_snapshot(self, db_with_sample_data, sample_snapshot_data):
        """Test upsert logic for snapshots"""
        # Get district ID
        result = db_with_sample_data.execute(
            "SELECT id FROM districts"
        ).fetchone()
        district_id = result[0]
        
        # Upsert same snapshot again (should not create duplicate)
        db_with_sample_data.execute(
            """
            INSERT INTO mgnrega_snapshots
            (district_id, year, month, people_benefited, workdays_created)
            VALUES (:district_id, :year, :month, :people, :workdays)
            ON CONFLICT (district_id, year, month) DO NOTHING
            """,
            {
                "district_id": district_id,
                "year": sample_snapshot_data["year"],
                "month": sample_snapshot_data["month"],
                "people": sample_snapshot_data["people_benefited"],
                "workdays": sample_snapshot_data["workdays_created"]
            }
        )
        db_with_sample_data.commit()
        
        # Verify only one record exists
        count = db_with_sample_data.execute(
            "SELECT COUNT(*) FROM mgnrega_snapshots"
        ).scalar()
        
        assert count == 1
    
    def test_query_districts(self, db_with_sample_data):
        """Test querying districts from database"""
        result = db_with_sample_data.execute(
            "SELECT COUNT(*) FROM districts"
        ).scalar()
        
        assert result >= 1
    
    def test_query_snapshots(self, db_with_sample_data):
        """Test querying snapshots from database"""
        result = db_with_sample_data.execute(
            "SELECT COUNT(*) FROM mgnrega_snapshots"
        ).scalar()
        
        assert result >= 1

