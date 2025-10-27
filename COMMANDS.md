# 🚀 Quick Command Reference

## Getting Started

```bash
# Clone and setup
git clone <repo-url>
cd our-voice-our-rights

# Start all services
docker-compose up -d

# Seed database
docker-compose exec ingest python seed_districts.py

# Run data ingestion
docker-compose exec ingest python worker.py
```

## Common Commands

### Docker Management

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Restart services
docker-compose restart

# Rebuild after code changes
docker-compose up -d --build

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Database Commands

```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U mgnrega_user -d mgnrega_db

# Run SQL query
docker-compose exec postgres psql -U mgnrega_user -d mgnrega_db -c "SELECT COUNT(*) FROM districts;"

# Check tables
docker-compose exec postgres psql -U mgnrega_user -d mgnrega_db -c "\dt"

# Backup database
docker-compose exec postgres pg_dump -U mgnrega_user mgnrega_db > backup.sql

# Restore database
docker-compose exec -T postgres psql -U mgnrega_user mgnrega_db < backup.sql
```

### Redis Commands

```bash
# Connect to Redis CLI
docker-compose exec redis redis-cli

# Check Redis is running
docker-compose exec redis redis-cli ping
# Expected: PONG

# List all keys
docker-compose exec redis redis-cli KEYS '*'

# Clear cache
docker-compose exec redis redis-cli FLUSHALL

# Get specific key
docker-compose exec redis redis-cli GET "districts:state:all"
```

### Testing

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test API endpoints
curl http://localhost:8000/api/v1/districts/states

# Run integration tests
cd backend
pytest test_api.py -v

# Run all validation scripts
bash scripts/validate_all.sh
```

### Ingestion

```bash
# Seed districts (first time)
docker-compose exec ingest python seed_districts.py

# Ingest current month data for all districts
docker-compose exec ingest python worker.py

# Ingest for specific district
docker-compose exec ingest python worker.py UP-LUC

# Ingest for specific month
docker-compose exec ingest python worker.py UP-LUC 2025 3
```

### Development

```bash
# Backend development
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend development
cd frontend
npm install
npm run dev
```

## Validation Commands

```bash
# Complete validation (Linux/Mac)
bash scripts/validate_all.sh

# Complete validation (Windows)
# Run scripts manually in PowerShell

# Individual validations
bash scripts/validate_backend.sh
bash scripts/validate_database.sh
bash scripts/validate_ingest.sh
```

## Troubleshooting

```bash
# Check container status
docker-compose ps

# Check if ports are in use
netstat -an | findstr :8000  # Windows
lsof -i :8000                # Mac/Linux

# Reset everything
docker-compose down -v
docker-compose up -d --build
docker-compose exec ingest python seed_districts.py

# View detailed logs
docker-compose logs backend --tail=100
docker-compose logs frontend --tail=100
```

## Production Deployment

```bash
# Set production environment
export ENVIRONMENT=production
export DEBUG=false

# Build and push to registry
docker-compose build
docker tag our-voice-our-rights-frontend your-registry/frontend:latest
docker tag our-voice-our-rights-backend your-registry/backend:latest
docker push your-registry/frontend:latest
docker push your-registry/backend:latest

# Deploy with environment variables
docker run -d \
  -e DATABASE_URL=... \
  -e REDIS_URL=... \
  -p 8080:80 \
  your-registry/frontend:latest
```

## Access Points

- Frontend: http://localhost:8080
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health Check: http://localhost:8000/health

## Git Commands

```bash
# After validation step
git add .
git commit -m "chore: validation step X complete"

# Push to repository
git push origin main

# Create feature branch
git checkout -b feature/new-feature

# Merge changes
git checkout main
git merge feature/new-feature
```

