@echo off
REM Database Validation Script for Windows
setlocal enabledelayedexpansion

echo =========================================
echo 🔍 Validating Database
echo =========================================

REM Check PostgreSQL container
echo ✅ Checking PostgreSQL container...
docker ps | findstr postgres
if %errorlevel% neq 0 (
    echo ❌ PostgreSQL container not running!
    exit /b 1
)

REM Check Redis
echo.
echo ✅ Checking Redis...
docker-compose exec redis redis-cli ping
if %errorlevel% neq 0 (
    echo ❌ Redis ping failed!
    exit /b 1
) else (
    echo ✅ Redis is operational!
)

echo.
echo =========================================
echo ✅ Database and cache validated!
echo =========================================

