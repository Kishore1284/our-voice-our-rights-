# Our Voice, Our Rights - MGNREGA Transparency Dashboard

![Status](https://img.shields.io/badge/status-active-success) ![License](https://img.shields.io/badge/license-MIT-blue) ![Python](https://img.shields.io/badge/python-3.11-blue) ![React](https://img.shields.io/badge/react-18.2-blue)

A production-ready web application for tracking MGNREGA (Mahatma Gandhi National Rural Employment Guarantee Act) performance metrics in real-time. Built as a Digital India Initiative with a focus on transparency and accessibility.

## 🌟 Features

- ✅ **Live Data Visualization** - Real-time MGNREGA statistics from data.gov.in
- 📊 **Interactive Dashboards** - District-wise performance metrics with trend charts
- 🔊 **Audio Guide** - Text-to-speech support in Hindi & English for low-literacy users
- 📱 **Mobile-First Design** - Optimized for all devices and 2G/3G networks
- 🗺️ **Geolocation Support** - Automatic district detection based on your location
- 📈 **Trend Analysis** - Track performance over the last 6 months
- 🎨 **Modern UI** - Beautiful gradient design with TailwindCSS
- ⚡ **Fast Performance** - Redis caching and optimized database queries
- ♿ **Accessible** - WCAG AA compliant with high contrast colors

## 🏗️ Architecture

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│  Frontend   │◄────────┤   Nginx     │◄────────┤    Users    │
│  (React)    │  Port 80│  (Reverse   │  HTTPS  │  (Browser)  │
│   Vite      │         │   Proxy)    │         │             │
└─────────────┘         └─────────────┘         └─────────────┘
       │                       │
       │                       ▼
       │                ┌─────────────┐
       │                │   Backend   │
       └───────────────►│  (FastAPI)  │
                  API  │   Port 8000  │
                   80  └─────────────┘
                               │
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
          ▼                    ▼                    ▼
   ┌───────────┐       ┌───────────┐        ┌─────────────┐
   │ PostgreSQL│       │   Redis   │        │  Ingestion  │
   │     :5432 │       │   :6379   │        │   Worker    │
   └───────────┘       └───────────┘        └─────────────┘
```

## 🔍 Post-Build Validation

Complete validation suite included! See:
- `VALIDATION_GUIDE.md` - Step-by-step validation steps
- `VALIDATION_SUMMARY.md` - Checklist summary
- `scripts/validate_all.sh` - Automated validation script

**Quick validation:**
```bash
# Run all validation checks
bash scripts/validate_all.sh

# Or validate step-by-step
bash scripts/validate_backend.sh
bash scripts/validate_database.sh
bash scripts/validate_ingest.sh
```

## 🚀 Quick Start

### Prerequisites

- Docker 20.10+
- Docker Compose 2.0+

### Step 1: Clone and Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/our-voice-our-rights.git
cd our-voice-our-rights

# Copy environment variables
cp .env.example .env

# Edit .env and add your MGNREGA API key (free from data.gov.in)
```

### Step 2: Start Services

```bash
# Start all services
docker-compose up -d

# Check logs
docker-compose logs -f
```

### Step 3: Seed Database

```bash
# Seed districts and sample data
docker-compose exec ingest python seed_districts.py

# Ingest current month data
docker-compose exec ingest python worker.py
```

### Step 4: Access the Application

- **Frontend**: http://localhost:8080
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Database**: localhost:5432

## 📁 Project Structure

```
our-voice-our-rights/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app
│   │   ├── config.py             # Settings
│   │   ├── database.py           # DB connection
│   │   ├── models.py             # SQLAlchemy models
│   │   ├── schemas.py            # Pydantic schemas
│   │   ├── cache.py              # Redis utilities
│   │   └── routers/
│   │       ├── districts.py      # Districts API
│   │       └── geolocate.py      # Geolocation API
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── App.jsx               # Main app
│   │   ├── main.jsx              # Entry point
│   │   ├── components/
│   │   │   ├── LocationSelector.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── MetricCard.jsx
│   │   │   └── TrendChart.jsx
│   │   ├── services/
│   │   │   └── api.js            # API client
│   │   └── utils/
│   │       └── speech.js         # TTS utilities
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── Dockerfile
├── ingest/
│   ├── worker.py                 # Data ingestion
│   ├── seed_districts.py         # Database seeder
│   └── Dockerfile
├── docker-compose.yml
├── init.sql                       # Database schema
└── README.md
```

## 🗄️ Database Schema

### Tables

#### `districts`
- `id` - Primary key
- `state` - State name
- `district_name` - District name
- `district_code` - Unique code (e.g., "UP-LUC")
- `latitude`, `longitude` - Coordinates for geolocation
- `created_at` - Timestamp

#### `mgnrega_snapshots`
- `id` - Primary key
- `district_id` - Foreign key to districts
- `year`, `month` - Time period
- `people_benefited` - Total people benefited
- `workdays_created` - Workdays created
- `wages_paid` - Total wages (₹)
- `payments_on_time_percent` - Payment timeliness (%)
- `works_completed` - Completed works
- `raw_json` - Original API response (JSONB)
- `fetched_at` - Timestamp

### Indexes
- Index on `districts.state` and `districts.district_code`
- Index on `mgnrega_snapshots.district_id`, `(year, month)`

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/districts` | List all districts (optional `?state=` filter) |
| GET | `/api/v1/districts/states` | List all states with district counts |
| GET | `/api/v1/districts/{code}/snapshot` | Get latest snapshot with comparison |
| GET | `/api/v1/districts/{code}/trend?months=6` | Get trend data (last N months) |
| POST | `/api/v1/geolocate` | Find nearest district (lat/lon) |
| GET | `/health` | Health check |
| GET | `/docs` | Interactive API documentation |

## 📊 Data Ingestion

### Automated Ingestion

```bash
# Run worker for current month (all districts)
docker-compose exec ingest python worker.py

# Run for specific district
docker-compose exec ingest python worker.py UP-LUC

# Run for specific month
docker-compose exec ingest python worker.py UP-LUC 2025 3
```

### Cron Setup (Optional)

Add to crontab for daily updates:

```bash
# Daily at 2 AM
0 2 * * * docker-compose exec -T ingest python worker.py
```

## 🚢 Production Deployment

### Deploy to VPS

```bash
# 1. Clone on server
ssh user@your-server.com
git clone https://github.com/yourusername/our-voice-our-rights.git
cd our-voice-our-rights

# 2. Setup environment
cp .env.example .env
nano .env  # Edit with production values

# 3. Start services
docker-compose -f docker-compose.yml up -d --build

# 4. Setup Nginx reverse proxy
sudo apt-get install nginx
sudo nano /etc/nginx/sites-available/mgnrega

# Nginx config:
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# 5. Enable site
sudo ln -s /etc/nginx/sites-available/mgnrega /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# 6. Setup SSL (Let's Encrypt)
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `POSTGRES_USER` | Database user | `mgnrega_user` |
| `POSTGRES_PASSWORD` | Database password | `mgnrega_pass` |
| `POSTGRES_DB` | Database name | `mgnrega_db` |
| `REDIS_URL` | Redis connection URL | `redis://redis:6379/0` |
| `MGNREGA_API_KEY` | data.gov.in API key | Required |
| `VITE_API_BASE_URL` | Frontend API URL | `http://localhost:8000` |

## 🧪 Testing

Complete testing suite with unit, integration, and E2E tests.

**Quick test commands:**
```bash
# Backend tests
cd backend && pytest

# Frontend tests
cd frontend && npm test

# E2E tests
cd frontend && npm run test:e2e

# Coverage reports
cd backend && pytest --cov=app --cov-report=html
cd frontend && npm run test:coverage
```

**See `TESTING_GUIDE.md` for complete testing documentation.**

## 🛠️ Development

### Local Development

```bash
# Start database and cache only
docker-compose up -d postgres redis

# Backend (Terminal 1)
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (Terminal 2)
cd frontend
npm install
npm run dev

# Access at http://localhost:3000
```

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 📊 Monitoring & Logs

```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Check database
docker-compose exec postgres psql -U mgnrega_user -d mgnrega_db

# Check Redis cache
docker-compose exec redis redis-cli
> KEYS *
> GET "districts:state:all"
```

## 🐛 Troubleshooting

### Common Issues

**Issue**: Database connection errors
```bash
# Check if postgres is running
docker-compose ps postgres

# Reset database
docker-compose down -v
docker-compose up -d
```

**Issue**: CORS errors
```bash
# Check backend CORS settings in app/main.py
# Ensure VITE_API_BASE_URL is set correctly
```

**Issue**: Redis connection errors
```bash
# Restart Redis
docker-compose restart redis

# Check Redis logs
docker-compose logs redis
```

**Issue**: Frontend build fails
```bash
# Clear node_modules and rebuild
cd frontend
rm -rf node_modules dist
npm install
npm run build
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Digital India Initiative
- data.gov.in for MGNREGA data
- FastAPI, React, and TailwindCSS communities

---

**Made with 🇮🇳 for transparency and accessibility**
