"""
Seed Districts Database
Inserts district data and sample snapshots
"""

import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import random

DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'postgresql://mgnrega_user:mgnrega_pass@localhost:5432/mgnrega_db'
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Uttar Pradesh districts with coordinates
UP_DISTRICTS = [
    ('Uttar Pradesh', 'Lucknow', 'UP-LUC', 26.8467, 80.9462),
    ('Uttar Pradesh', 'Kanpur Nagar', 'UP-KAN', 26.4499, 80.3319),
    ('Uttar Pradesh', 'Ghaziabad', 'UP-GHA', 28.6692, 77.4538),
    ('Uttar Pradesh', 'Agra', 'UP-AGR', 27.1767, 78.0081),
    ('Uttar Pradesh', 'Varanasi', 'UP-VAR', 25.3176, 82.9739),
    ('Uttar Pradesh', 'Meerut', 'UP-MER', 28.9845, 77.7064),
    ('Uttar Pradesh', 'Allahabad', 'UP-ALL', 25.4484, 81.8333),
    ('Uttar Pradesh', 'Bareilly', 'UP-BAR', 28.3670, 79.4304),
    ('Uttar Pradesh', 'Gorakhpur', 'UP-GOR', 26.7588, 83.3697),
    ('Uttar Pradesh', 'Aligarh', 'UP-ALI', 27.8974, 78.0880),
    ('Uttar Pradesh', 'Saharanpur', 'UP-SAH', 29.9675, 77.5537),
    ('Uttar Pradesh', 'Moradabad', 'UP-MOR', 28.8384, 78.7728),
    ('Uttar Pradesh', 'Firozabad', 'UP-FIR', 27.1505, 78.3958),
    ('Uttar Pradesh', 'Mathura', 'UP-MAT', 27.4924, 77.6736),
    ('Uttar Pradesh', 'Ayodhya', 'UP-AYO', 26.7921, 82.2036),
]


def seed_districts():
    """
    Insert districts into database
    """
    print("\n" + "="*60)
    print("  SEEDING DISTRICTS")
    print("="*60 + "\n")
    
    session = SessionLocal()
    inserted = 0
    skipped = 0
    
    try:
        for state, name, code, lat, lon in UP_DISTRICTS:
            try:
                session.execute(
                    text("""
                        INSERT INTO districts 
                        (state, district_name, district_code, latitude, longitude)
                        VALUES (:state, :name, :code, :lat, :lon)
                        ON CONFLICT (district_code) DO NOTHING
                    """),
                    {'state': state, 'name': name, 'code': code, 'lat': lat, 'lon': lon}
                )
                session.commit()
                
                # Check if inserted
                result = session.execute(
                    text("SELECT COUNT(*) FROM districts WHERE district_code = :code"),
                    {'code': code}
                ).scalar()
                
                if result > 0:
                    print(f"✓ {code} - {name}")
                    inserted += 1
                else:
                    print(f"⊙ {code} - {name} (skipped)")
                    skipped += 1
                    
            except Exception as e:
                print(f"✗ {code} - {name}: {e}")
                session.rollback()
        
        print(f"\n Inserted: {inserted}, Skipped: {skipped}")
        
    finally:
        session.close()


def seed_sample_snapshots():
    """
    Generate sample snapshots for last 6 months
    """
    print("\n" + "="*60)
    print("  GENERATING SAMPLE SNAPSHOTS")
    print("="*60 + "\n")
    
    session = SessionLocal()
    
    try:
        # Get all districts
        result = session.execute(text("SELECT id FROM districts"))
        district_ids = [row[0] for row in result.fetchall()]
        
        now = datetime.now()
        current_year = now.year
        current_month = now.month
        
        for district_id in district_ids:
            for i in range(6):
                month = current_month - i
                year = current_year
                
                # Handle year rollover
                while month <= 0:
                    month += 12
                    year -= 1
                
                # Generate random but realistic data
                base_people = random.randint(35000, 55000)
                workdays = base_people * random.randint(18, 22)
                wages = workdays * 176
                payments_on_time = random.uniform(85, 98)
                works_completed = random.randint(250, 450)
                
                try:
                    session.execute(
                        text("""
                            INSERT INTO mgnrega_snapshots
                            (district_id, year, month, people_benefited, workdays_created,
                             wages_paid, payments_on_time_percent, works_completed)
                            VALUES (:district_id, :year, :month, :people, :workdays,
                                    :wages, :payments, :works)
                            ON CONFLICT DO NOTHING
                        """),
                        {
                            'district_id': district_id,
                            'year': year,
                            'month': month,
                            'people': base_people,
                            'workdays': workdays,
                            'wages': float(wages),
                            'payments': float(payments_on_time),
                            'works': works_completed
                        }
                    )
                except Exception as e:
                    print(f"✗ Error for district {district_id}, {year}/{month}: {e}")
            
            session.commit()
            print(f"✓ Generated 6 months of data for district {district_id}")
        
        print("\n Sample snapshot generation complete!")
        
    finally:
        session.close()


if __name__ == '__main__':
    print("\n" + "="*60)
    print("  MGNREGA DATABASE SEEDER")
    print("  Our Voice, Our Rights - Digital India Initiative")
    print("="*60)
    
    seed_districts()
    seed_sample_snapshots()
    
    print("\n" + "="*60)
    print("  SEEDING COMPLETE!")
    print("="*60 + "\n")

