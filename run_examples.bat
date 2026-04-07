@echo off
REM ViralLens AI - Example Usage Script for Windows

setlocal enabledelayedexpansion

echo.
echo ╔════════════════════════════════════════════════════════════════════════════╗
echo ║        ViralLens AI - FastAPI Examples ^& API Testing                       ║
echo ╚════════════════════════════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if the API is running
echo [*] Checking if API server is running...
curl -s http://localhost:8000/health >nul 2>&1
if errorlevel 1 (
    echo ❌ API server is not running at http://localhost:8000
    echo.
    echo Please start the API server first using:
    echo   run_server.bat
    echo or
    echo   uvicorn main:app --reload
    pause
    exit /b 1
)

echo ✓ API server is up and running!
echo.

REM Check if requests library is installed
echo [*] Checking dependencies...
python -c "import requests" 2>nul
if errorlevel 1 (
    echo ❌ Requests library not installed
    echo [*] Installing...
    pip install requests
    if errorlevel 1 (
        echo ❌ Failed to install requests
        pause
        exit /b 1
    )
)

echo.
echo [*] Running examples...
echo.

REM Run examples
python example_usage.py
if errorlevel 1 (
    echo ❌ Failed to run examples
    pause
    exit /b 1
)

echo.
echo Examples completed successfully!
echo.
echo For more information, check:
echo   • API Documentation: http://localhost:8000/docs
echo   • README: README.md
echo   • API Guide: API_GUIDE.md
echo.

pause
