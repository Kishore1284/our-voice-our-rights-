"""
MGNREGA Data Ingestion Worker
Fetches data from MGNREGA API and stores in database
"""

import os
import sys
import time
import random
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import redis
from redis import Redis

# Database configuration
DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'postgresql://mgnrega_user:mgnrega_pass@localhost:5432/mgnrega_db'
)
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
API_KEY = os.getenv('MGNREGA_API_KEY', '')

# Initialize connections
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
redis_client = Redis.from_url(REDIS_URL, decode_responses=True)


def fetch_mgnrega_data(district_code, year, month):
    """
    Fetch MGNREGA data from API or generate mock data
    
    TODO: Implement actual API call to data.gov.in when API is available
    """
    # Generate realistic mock data for now
    base_people = random.randint(35000, 55000)
    workdays = base_people * 20
    wages = workdays * 176  # Average wage per day
    payments_on_time = random.uniform(85, 98)
    works_completed = random.randint(250, 450)
    
    return {
        'people_benefited': base_people,
        'workdays_created': workdays,
        'wages_paid': float(wages),
        'payments_on_time_percent': float(payments_on_time),
        'works_completed': works_completed,
        'raw_json': {
            'district_code': district_code,
            'year': year,
            'month': month,
            'source': 'mock_data'
        }
    }


def store_snapshot(session, district_id, year, month, data):
    """
    Store or update snapshot in database
    """
    try:
        # Use ON CONFLICT UPDATE for upsert
        query = text("""
            INSERT INTO mgnrega_snapshots 
            (district_id, year, month, people_benefited, workdays_created, 
             wages_paid, payments_on_time_percent, works_completed, raw_json)
            VALUES (:district_id, :year, :month, :people_benefited, :workdays_created,
                    :wages_paid, :payments_on_time_percent, :works_completed, 
                    :raw_json::jsonb)
            ON CONFLICT (district_id, year, month) 
            DO UPDATE SET 
                people_benefited = EXCLUDED.people_benefited,
                workdays_created = EXCLUDED.workdays_created,
                wages_paid = EXCLUDED.wages_paid,
                payments_on_time_percent = EXCLUDED.payments_on_time_percent,
                works_completed = EXCLUDED.works_completed,
                raw_json = EXCLUDED.raw_json,
                fetched_at = CURRENT_TIMESTAMP
        """)
        
        session.execute(query, {
            'district_id': district_id,
            'year': year,
            'month': month,
            'people_benefited': data['people_benefited'],
            'workdays_created': data['workdays_created'],
            'wages_paid': data['wages_paid'],
            'payments_on_time_percent': data['payments_on_time_percent'],
            'works_completed': data['works_completed'],
            'raw_json': str(data['raw_json'])
        })
        
        session.commit()
        
        # Clear cache for this district
        redis_client.delete(f"district:snapshot:{district_id}")
        redis_client.delete(f"district:trend:{district_id}:*")
        
        return True
    except Exception as e:
        session.rollback()
        print(f"✗ Error storing snapshot: {e}")
        return False


def ingest_all_districts():
    """
    Ingest data for all districts
    """
    print("\n" + "="*60)
    print("  MGNREGA DATA INGESTION WORKER")
    print("="*60 + "\n")
    
    session = SessionLocal()
    
    try:
        # Get current year and month
        now = datetime.now()
        year = now.year
        month = now.month
        
        # Get all districts
        result = session.execute(text("SELECT id, district_code FROM districts"))
        districts = result.fetchall()
        
        print(f"Ingesting data for {len(districts)} districts...")
        print(f"Month: {month}/{year}\n")
        
        success_count = 0
        error_count = 0
        
        for district_id, district_code in districts:
            try:
                data = fetch_mgnrega_data(district_code, year, month)
                if store_snapshot(session, district_id, year, month, data):
                    print(f"✓ {district_code}")
                    success_count += 1
                else:
                    print(f"✗ {district_code} (storage failed)")
                    error_count += 1
                
                time.sleep(0.5)  # Rate limiting
                
            except Exception as e:
                print(f"✗ {district_code}: {e}")
                error_count += 1
        
        print(f"\n{'='*60}")
        print(f"  Summary: {success_count} successful, {error_count} errors")
        print("="*60 + "\n")
        
    finally:
        session.close()


def ingest_single_district(district_code, year=None, month=None):
    """
    Ingest data for a single district
    """
    if year is None or month is None:
        now = datetime.now()
        year = year or now.year
        month = month or now.month
    
    session = SessionLocal()
    
    try:
        result = session.execute(
            text("SELECT id FROM districts WHERE district_code = :code"),
            {'code': district_code}
        )
        district = result.fetchone()
        
        if not district:
            print(f"✗ District '{district_code}' not found")
            return
        
        district_id = district[0]
        data = fetch_mgnrega_data(district_code, year, month)
        
        if store_snapshot(session, district_id, year, month, data):
            print(f"✓ Ingested data for {district_code}")
        else:
            print(f"✗ Failed to ingest data for {district_code}")
            
    finally:
        session.close()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Single district mode
        district_code = sys.argv[1]
        year = int(sys.argv[2]) if len(sys.argv) > 2 else None
        month = int(sys.argv[3]) if len(sys.argv) > 3 else None
        ingest_single_district(district_code, year, month)
    else:
        # All districts mode
        ingest_all_districts()

