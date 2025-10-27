-- ============================================================================
-- MGNREGA Transparency Dashboard - Database Schema
-- Our Voice, Our Rights - Digital India Initiative
-- ============================================================================

-- Enable UUID extension (if needed for future enhancements)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================================
-- TABLE: districts
-- Stores district information with geolocation data
-- ============================================================================
CREATE TABLE IF NOT EXISTS districts (
    id SERIAL PRIMARY KEY,
    state TEXT NOT NULL,
    district_name TEXT NOT NULL,
    district_code TEXT UNIQUE NOT NULL,
    latitude NUMERIC(10, 8),
    longitude NUMERIC(11, 8),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for districts table
CREATE INDEX IF NOT EXISTS idx_districts_state ON districts(state);
CREATE INDEX IF NOT EXISTS idx_districts_code ON districts(district_code);
CREATE INDEX IF NOT EXISTS idx_districts_coords ON districts(latitude, longitude);

-- ============================================================================
-- TABLE: mgnrega_snapshots
-- Stores MGNREGA performance data snapshots by month
-- ============================================================================
CREATE TABLE IF NOT EXISTS mgnrega_snapshots (
    id SERIAL PRIMARY KEY,
    district_id INTEGER NOT NULL REFERENCES districts(id) ON DELETE CASCADE,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL CHECK (month >= 1 AND month <= 12),
    people_benefited INTEGER DEFAULT 0,
    workdays_created INTEGER DEFAULT 0,
    wages_paid NUMERIC(15, 2) DEFAULT 0,
    payments_on_time_percent NUMERIC(5, 2) DEFAULT 0,
    works_completed INTEGER DEFAULT 0,
    raw_json JSONB,
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (district_id, year, month)
);

-- Create indexes for mgnrega_snapshots table
CREATE INDEX IF NOT EXISTS idx_snapshots_district ON mgnrega_snapshots(district_id);
CREATE INDEX IF NOT EXISTS idx_snapshots_year_month ON mgnrega_snapshots(year, month);
CREATE INDEX IF NOT EXISTS idx_snapshots_fetched ON mgnrega_snapshots(fetched_at);
CREATE INDEX IF NOT EXISTS idx_snapshots_composite ON mgnrega_snapshots(district_id, year DESC, month DESC);

-- ============================================================================
-- VIEW: latest_district_snapshots
-- Provides the latest snapshot for each district with district info
-- ============================================================================
CREATE OR REPLACE VIEW latest_district_snapshots AS
SELECT 
    d.id as district_id,
    d.state,
    d.district_name,
    d.district_code,
    d.latitude,
    d.longitude,
    s.year,
    s.month,
    s.people_benefited,
    s.workdays_created,
    s.wages_paid,
    s.payments_on_time_percent,
    s.works_completed,
    s.fetched_at
FROM districts d
LEFT JOIN LATERAL (
    SELECT * FROM mgnrega_snapshots 
    WHERE district_id = d.id 
    ORDER BY year DESC, month DESC 
    LIMIT 1
) s ON true;

-- ============================================================================
-- SAMPLE DATA: Uttar Pradesh Districts
-- Insert 10 Uttar Pradesh districts with geographic coordinates
-- ============================================================================
INSERT INTO districts (state, district_name, district_code, latitude, longitude) VALUES
('Uttar Pradesh', 'Lucknow', 'UP-LUC', 26.8467, 80.9462),
('Uttar Pradesh', 'Kanpur Nagar', 'UP-KAN', 26.4499, 80.3319),
('Uttar Pradesh', 'Ghaziabad', 'UP-GHA', 28.6692, 77.4538),
('Uttar Pradesh', 'Agra', 'UP-AGR', 27.1767, 78.0081),
('Uttar Pradesh', 'Varanasi', 'UP-VAR', 25.3176, 82.9739),
('Uttar Pradesh', 'Meerut', 'UP-MER', 28.9845, 77.7064),
('Uttar Pradesh', 'Allahabad', 'UP-ALL', 25.4484, 81.8333),
('Uttar Pradesh', 'Bareilly', 'UP-BAR', 28.3670, 79.4304),
('Uttar Pradesh', 'Gorakhpur', 'UP-GOR', 26.7588, 83.3697),
('Uttar Pradesh', 'Aligarh', 'UP-ALI', 27.8974, 78.0880)
ON CONFLICT (district_code) DO NOTHING;

-- ============================================================================
-- Comments and documentation
-- ============================================================================
COMMENT ON TABLE districts IS 'Stores district information with geolocation for MGNREGA tracking';
COMMENT ON TABLE mgnrega_snapshots IS 'Monthly snapshots of MGNREGA performance data per district';
COMMENT ON COLUMN districts.latitude IS 'Decimal degrees latitude for geolocation';
COMMENT ON COLUMN districts.longitude IS 'Decimal degrees longitude for geolocation';
COMMENT ON COLUMN mgnrega_snapshots.year IS 'Fiscal or calendar year of snapshot';
COMMENT ON COLUMN mgnrega_snapshots.month IS 'Month number 1-12';
COMMENT ON COLUMN mgnrega_snapshots.raw_json IS 'Original API response stored as JSONB for audit';

