# 🧪 Testing Guide

## Complete Testing Strategy

This document outlines the comprehensive testing system for the MGNREGA platform.

## 📋 Test Structure

```
backend/
├── tests/
│   ├── unit/           # Fast unit tests with mocks
│   │   ├── test_health.py
│   │   ├── test_cache.py
│   │   ├── test_database.py
│   │   └── test_schemas.py
│   └── integration/    # Tests with real DB
│       └── test_api_with_db.py

ingest/
└── tests/
    └── test_worker.py

frontend/
├── src/
│   ├── test/
│   │   ├── setup.js
│   │   └── mocks/
│   └── components/
│       └── __tests__/
│           ├── LocationSelector.test.jsx
│           └── MetricCard.test.jsx
└── tests/
    └── e2e/
        └── homepage.spec.js
```

## 🚀 Running Tests

### Backend Tests

```bash
# Navigate to backend
cd backend

# Install dependencies
pip install -r requirements.txt

# Run all tests
pytest

# Run unit tests only
pytest tests/unit -v

# Run integration tests
pytest tests/integration -v

# Run with coverage
pytest --cov=app --cov-report=html

# View coverage report
open htmlcov/index.html  # Mac
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### Ingestion Worker Tests

```bash
# Navigate to ingest
cd ingest

# Install dependencies
pip install -r requirements.txt pytest

# Run tests
pytest tests/ -v
```

### Frontend Tests

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Run unit tests
npm test

# Run tests with UI
npm run test:ui

# Run with coverage
npm run test:coverage

# Run E2E tests (requires app running)
npm run test:e2e

# Run E2E with UI
npm run test:e2e:ui
```

## 📊 Test Coverage Goals

| Layer | Target Coverage |
|-------|----------------|
| Backend API | 85%+ |
| Frontend Components | 80%+ |
| Ingestion Worker | 75%+ |
| Integration Tests | 90%+ |

## 🧪 Test Types

### 1. Unit Tests (Fast)

**Location:** `backend/tests/unit/`

**Purpose:** Test individual functions in isolation with mocked dependencies.

**Examples:**
- Health endpoint returns `{"status": "ok"}`
- Cache set/get operations work correctly
- Schema validation with Pydantic
- Database utility functions

**Running:**
```bash
cd backend
pytest tests/unit -v
```

### 2. Integration Tests

**Location:** `backend/tests/integration/`

**Purpose:** Test API endpoints with real database connection (SQLite in-memory).

**Examples:**
- API endpoints return correct JSON schemas
- Database queries execute successfully
- Cache integration (first miss, second hit)
- Error handling for invalid requests

**Running:**
```bash
cd backend
pytest tests/integration -v
```

### 3. Ingestion Worker Tests

**Location:** `ingest/tests/`

**Purpose:** Test data fetching and database upsert logic.

**Examples:**
- Mock API calls return realistic data
- Snapshot upsert doesn't create duplicates
- Error handling for rate limits (429)
- Invalid data handling

**Running:**
```bash
cd ingest
pytest tests/ -v
```

### 4. Frontend Component Tests

**Location:** `frontend/src/components/__tests__/`

**Purpose:** Test React components with mocked APIs.

**Examples:**
- Components render correctly
- User interactions trigger expected behavior
- TTS button calls speech synthesis
- Loading states display properly

**Running:**
```bash
cd frontend
npm test
```

### 5. End-to-End Tests

**Location:** `frontend/tests/e2e/`

**Purpose:** Test full user workflows with real browser.

**Examples:**
- User visits homepage
- Location selection works
- Dashboard loads with data
- TTS triggers on button click

**Running:**
```bash
cd frontend
npm run test:e2e
```

## 🔧 Test Configuration

### Backend (`pytest.ini`)

```ini
[pytest]
testpaths = tests
python_files = test_*.py
addopts = 
    -v
    --cov=app
    --cov-report=html
    --cov-fail-under=85
markers =
    unit: Unit tests
    integration: Integration tests
```

### Frontend (`vitest.config.js`)

```javascript
export default defineConfig({
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./src/test/setup.js'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html']
    }
  }
})
```

## 📈 Coverage Reports

### Viewing Coverage

**Backend:**
```bash
cd backend
pytest --cov=app --cov-report=html
open htmlcov/index.html
```

**Frontend:**
```bash
cd frontend
npm run test:coverage
open coverage/index.html
```

### Coverage Thresholds

Enforced in CI:
- **Backend**: Minimum 85% coverage
- **Frontend**: Minimum 80% coverage
- **Integration**: All tests must pass

## 🤖 CI/CD Integration

### GitHub Actions Workflow

Located at `.github/workflows/ci.yml`

**Jobs:**
1. **Backend Tests** - Python 3.11, unit + integration tests
2. **Ingestion Tests** - Worker function tests
3. **Frontend Tests** - Node 18.x and 20.x, Vitest
4. **E2E Tests** - Playwright with Docker Compose
5. **Build Check** - Verify Docker builds work

**Running Locally:**
```bash
# Install act (GitHub Actions local runner)
brew install act  # Mac
# Or download from: https://github.com/nektos/act

# Run CI locally
act -j backend-tests
```

## 🐛 Debugging Tests

### Backend

```bash
# Run with verbose output
pytest -vv

# Run specific test file
pytest tests/unit/test_health.py -v

# Run specific test
pytest tests/unit/test_health.py::TestHealthEndpoint::test_health_check -v

# Drop into debugger on failure
pytest --pdb

# Show print statements
pytest -s
```

### Frontend

```bash
# Run tests in watch mode
npm test -- --watch

# Run with UI
npm run test:ui

# Debug specific test
npm test -- LocationSelector.test.jsx
```

### E2E

```bash
# Run in headed mode
npm run test:e2e -- --headed

# Debug mode
npm run test:e2e:ui

# Run specific test
npm run test:e2e -- homepage.spec.js
```

## ✅ Test Checklist

Before committing:

- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] Coverage above threshold (85% backend, 80% frontend)
- [ ] No skipped tests
- [ ] Linter passes
- [ ] Tests run in CI

## 📚 Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Vitest Documentation](https://vitest.dev/)
- [Playwright Documentation](https://playwright.dev/)
- [Testing Library](https://testing-library.com/)

---

**Happy Testing! 🎉**

