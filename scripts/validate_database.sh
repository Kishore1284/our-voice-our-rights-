#!/bin/bash
# Database Validation Script

set -e

echo "========================================="
echo "🔍 Validating Database"
echo "========================================="

# Check PostgreSQL container
echo "✅ Checking PostgreSQL container..."
docker ps | grep postgres || (echo "❌ PostgreSQL container not running!" && exit 1)

# Check if tables exist
echo "✅ Checking database tables..."
docker-compose exec -T postgres psql -U mgnrega_user -d mgnrega_db -c "\dt" | grep -q districts || (echo "❌ Districts table not found!" && exit 1)
docker-compose exec -T postgres psql -U mgnrega_user -d mgnrega_db -c "\dt" | grep -q mgnrega_snapshots || (echo "❌ Snapshots table not found!" && exit 1)

echo "✅ Tables exist!"

# Check sample data
echo "✅ Checking sample data..."
DISTRICT_COUNT=$(docker-compose exec -T postgres psql -U mgnrega_user -d mgnrega_db -t -c "SELECT COUNT(*) FROM districts;")
echo "Districts in database: $DISTRICT_COUNT"

if [ "$DISTRICT_COUNT" -lt 5 ]; then
    echo "⚠️  Warning: Less than 5 districts found. Run seed script!"
fi

echo "✅ Database validation complete!"

# Check Redis
echo "✅ Checking Redis..."
REDIS_PING=$(docker-compose exec -T redis redis-cli ping)
if [ "$REDIS_PING" = "PONG" ]; then
    echo "✅ Redis is operational!"
else
    echo "❌ Redis ping failed!"
    exit 1
fi

echo "========================================="
echo "✅ Database and cache validated!"
echo "========================================="

