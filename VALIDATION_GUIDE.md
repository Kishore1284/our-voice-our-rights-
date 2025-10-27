# 🔍 Post-Build Validation Guide

Complete step-by-step validation checklist for MGNREGA platform.

## Prerequisites

```bash
# Ensure Docker is running
docker --version
docker-compose --version
```

## ✅ Checklist Execution

### Step 1: Backend Verification

```bash
# Start all services
docker-compose up -d

# Wait for services to be ready
sleep 10

# Test health endpoint
curl http://localhost:8000/health
# Expected: {"status":"ok"}

# Test API docs
curl http://localhost:8000/docs
# Expected: HTML page loads

# Test districts endpoint
curl http://localhost:8000/api/v1/districts/states
# Expected: JSON with states array

# Using automated script (Linux/Mac)
bash scripts/validate_backend.sh

# Using automated script (Windows)
scripts\validate_backend.bat
```

**Commit after success:**
```bash
git add .
git commit -m "chore: backend verified and health endpoint functional"
```

### Step 2: Database and Cache

```bash
# Check container health
docker-compose ps

# Should show all containers as "healthy"

# Connect to PostgreSQL
docker-compose exec postgres psql -U mgnrega_user -d mgnrega_db

# Inside psql:
\dt
# Should show: districts, mgnrega_snapshots

SELECT COUNT(*) FROM districts;
# Should return number > 0

\q

# Test Redis
docker-compose exec redis redis-cli ping
# Expected: PONG

# Using automated script
bash scripts/validate_database.sh
```

**Commit after success:**
```bash
git add .
git commit -m "chore: database + Redis verified operational"
```

### Step 3: Ingest Worker Validation

```bash
# Seed database with districts
docker-compose exec ingest python seed_districts.py

# Expected output:
# ============================================================
#   SEEDING DISTRICTS
# ✓ UP-LUC - Lucknow
# ✓ UP-KAN - Kanpur Nagar
# ... (more districts)

# Run ingestion worker
docker-compose exec ingest python worker.py

# Expected: "✓ Ingested..." messages for each district

# Verify data in database
docker-compose exec postgres psql -U mgnrega_user -d mgnrega_db \
  -c "SELECT COUNT(*) FROM mgnrega_snapshots;"

# Should return count > 0

# Using automated script
bash scripts/validate_ingest.sh
```

**Commit after success:**
```bash
git add .
git commit -m "chore: ingestion pipeline tested and DB populated"
```

### Step 4: Frontend Validation

```bash
# Start frontend (if not already running via docker-compose)
cd frontend
npm install
npm run dev

# Access in browser: http://localhost:5173
# or via Docker: http://localhost:8080

# Manual tests:
# 1. UI loads with district dropdown
# 2. "Use my location" button prompts for geolocation
# 3. Selecting district shows dashboard
# 4. Metric cards display data
# 5. Audio TTS works (click speaker icon)
# 6. Trend charts display
```

**Manual Test Checklist:**
- [ ] Homepage loads with district selector
- [ ] Location permission prompt appears on "Use My Location"
- [ ] Dashboard shows 5 metric cards
- [ ] Trend chart displays data
- [ ] TTS speaks metric values
- [ ] Mobile responsive design works

**Commit after success:**
```bash
git add .
git commit -m "chore: frontend verified functional with API"
```

### Step 5: Integration Tests

```bash
# Install test dependencies
cd backend
pip install -r requirements_test.txt

# Run tests
pytest test_api.py -v

# Expected output:
# ============================= test session starts
# test_api.py::TestHealthEndpoint::test_health_check PASSED
# test_api.py::TestDistrictsEndpoint::test_get_districts PASSED
# ...

# All tests should pass (PASSED or SKIPPED)
```

**Commit after success:**
```bash
git add .
git commit -m "test: integration tests passing for core endpoints"
```

### Step 6: Docker Compose Validation

```bash
# Stop all services
docker-compose down

# Rebuild and restart
docker-compose up --build -d

# Check all containers are healthy
docker-compose ps

# Expected: All containers show "(healthy)" status

# Test from Windows host (if using WSL)
curl http://localhost:8000/health
# Expected: {"status":"ok"}

# Access web app
# Open browser to: http://localhost:8080
```

**Commit after success:**
```bash
git add .
git commit -m "chore: docker-compose build verified"
```

### Step 7: Deployment Readiness

```bash
# Check environment variables
cat .env.example
# Ensure no hardcoded secrets

# Verify all secrets use environment variables
grep -r "password" backend/ --exclude="*.pyc"
# Should only show .env references

# Test with different environment
docker-compose exec backend env
# Should show DATABASE_URL, REDIS_URL, etc.

# Create production .env (for deployment)
cp .env.example .env.production
# Edit with production values
```

**Commit after success:**
```bash
git add .
git commit -m "docs: deployment verification complete"
```

### Step 8: Final Sanity Check

```bash
# Open in incognito browser
# 1. Go to http://localhost:8080
# 2. Verify no console errors
# 3. Test all features

# Run final API checks
curl http://localhost:8000/api/v1/districts/UP-LUC/snapshot
# Should return JSON with district data

# Check logs for errors
docker-compose logs backend | grep -i error

# If no errors, push to GitHub
git push origin main
```

## 🚨 Troubleshooting

### Issue: Backend won't start

```bash
# Check logs
docker-compose logs backend

# Common fixes:
# 1. Port 8000 already in use: Change port in docker-compose.yml
# 2. Database connection failed: Wait longer, check postgres health
# 3. Import errors: Check Python path in Dockerfile
```

### Issue: Database has no data

```bash
# Re-run seed script
docker-compose exec ingest python seed_districts.py

# Check if seed script ran successfully
docker-compose exec postgres psql -U mgnrega_user -d mgnrega_db \
  -c "SELECT COUNT(*) FROM districts;"
```

### Issue: Frontend can't connect to API

```bash
# Check CORS settings
docker-compose logs backend | grep CORS

# Check VITE_API_BASE_URL
echo $VITE_API_BASE_URL

# Verify backend is accessible
curl http://localhost:8000/health
```

## 📊 Expected Results

After completing all steps:

- ✅ Backend API responding with 200 status
- ✅ Database contains 15+ districts
- ✅ Redis cache operational
- ✅ Frontend loads without errors
- ✅ All API endpoints return valid JSON
- ✅ Integration tests pass
- ✅ Docker containers all healthy
- ✅ Ready for production deployment

## 🎯 Success Criteria

The application is production-ready when:

1. All automated tests pass
2. No errors in logs
3. API returns correct schemas
4. Frontend displays data correctly
5. Geolocation works
6. TTS speaks values
7. Charts render properly
8. Mobile responsive
9. Docker orchestration stable
10. Environment variables configured

---

**For detailed execution:**
- Run `bash scripts/validate_all.sh` (Linux/Mac)
- Or run scripts manually in order
- Each step commits progress independently

