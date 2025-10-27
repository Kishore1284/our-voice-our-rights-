# 🚀 Quick Start Guide

## Installation

### Prerequisites
- Docker 20.10+ and Docker Compose 2.0+

### Steps

1. **Start Services**
   ```bash
   docker-compose up -d
   ```

2. **Seed Database**
   ```bash
   docker-compose exec ingest python seed_districts.py
   ```

3. **Access Application**
   - Frontend: http://localhost:8080
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## Development Mode

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
# Access at http://localhost:3000
```

## Important Commands

```bash
# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Restart services
docker-compose restart

# Rebuild after code changes
docker-compose up -d --build

# Access database
docker-compose exec postgres psql -U mgnrega_user -d mgnrega_db
```

## Troubleshooting

If you encounter any issues:
1. Check logs: `docker-compose logs -f`
2. Restart services: `docker-compose restart`
3. Rebuild: `docker-compose up -d --build`
4. Full reset: `docker-compose down -v && docker-compose up -d`

