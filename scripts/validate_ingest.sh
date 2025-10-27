#!/bin/bash
# Ingest Worker Validation Script

set -e

echo "========================================="
echo "🔍 Validating Data Ingestion"
echo "========================================="

# Run seed script
echo "✅ Seeding database with districts..."
docker-compose exec -T ingest python seed_districts.py

# Run worker to fetch data
echo "✅ Running data ingestion worker..."
docker-compose exec -T ingest python worker.py || echo "⚠️  Some districts may have failed"

# Verify data in database
echo "✅ Verifying ingested data..."
SNAPSHOT_COUNT=$(docker-compose exec -T postgres psql -U mgnrega_user -d mgnrega_db -t -c "SELECT COUNT(*) FROM mgnrega_snapshots;")
echo "Snapshots in database: $SNAPSHOT_COUNT"

if [ "$SNAPSHOT_COUNT" -lt 1 ]; then
    echo "❌ No snapshots found! Ingestion failed!"
    exit 1
fi

echo "✅ Data ingestion validated!"

echo "========================================="
echo "✅ Ingestion pipeline complete!"
echo "========================================="

