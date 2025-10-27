@echo off
REM Backend Validation Script for Windows
setlocal enabledelayedexpansion

echo =========================================
echo 🔍 Validating Backend API
echo =========================================

REM Wait for backend to be ready
echo ⏳ Waiting for backend to be ready...
timeout /t 5 /nobreak >nul

REM Test health endpoint
echo ✅ Testing /health endpoint...
curl -s http://localhost:8000/health
if %errorlevel% neq 0 (
    echo ❌ Health endpoint failed!
    exit /b 1
)

echo.
echo ✅ Health endpoint working!

REM Test root endpoint
echo ✅ Testing root endpoint...
curl -s http://localhost:8000/

REM Test API endpoints
echo.
echo ✅ Testing /api/v1/districts/states...
curl -s http://localhost:8000/api/v1/districts/states

echo.
echo ✅ Testing /api/v1/districts...
curl -s http://localhost:8000/api/v1/districts

echo.
echo =========================================
echo ✅ Backend validation complete!
echo =========================================

