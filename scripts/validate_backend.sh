#!/bin/bash
# Backend Validation Script
# Run this after starting docker-compose

set -e

echo "========================================="
echo "🔍 Validating Backend API"
echo "========================================="

# Wait for backend to be ready
echo "⏳ Waiting for backend to be ready..."
sleep 5

# Test health endpoint
echo "✅ Testing /health endpoint..."
HEALTH_RESPONSE=$(curl -s http://localhost:8000/health)
echo "Response: $HEALTH_RESPONSE"

if echo "$HEALTH_RESPONSE" | grep -q "healthy"; then
    echo "✅ Health endpoint working!"
else
    echo "❌ Health endpoint failed!"
    exit 1
fi

# Test root endpoint
echo "✅ Testing root endpoint..."
ROOT_RESPONSE=$(curl -s http://localhost:8000/)
echo "Response: $ROOT_RESPONSE"

# Test API endpoints
echo "✅ Testing /api/v1/districts/states..."
STATES_RESPONSE=$(curl -s http://localhost:8000/api/v1/districts/states)
echo "Response: $STATES_RESPONSE"

echo "✅ Testing /api/v1/districts..."
DISTRICTS_RESPONSE=$(curl -s http://localhost:8000/api/v1/districts)
echo "Response: $DISTRICTS_RESPONSE"

echo "========================================="
echo "✅ Backend validation complete!"
echo "========================================="

