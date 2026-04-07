@echo off
REM ViralLens AI - FastAPI Server Startup Script for Windows

setlocal enabledelayedexpansion

echo.
echo ╔════════════════════════════════════════════════════════════════════════════╗
echo ║                   ViralLens AI - FastAPI Server                             ║
echo ╚════════════════════════════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if requirements are installed
echo [*] Checking dependencies...
python -c "import fastapi" 2>nul
if errorlevel 1 (
    echo ❌ FastAPI not installed
    echo [*] Installing dependencies from requirements.txt...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Check if models exist
echo [*] Checking for trained models...
set MISSING_MODELS=0

for %%A in (logistic_regression_pipeline.joblib random_forest_pipeline.joblib xgboost_pipeline.joblib viral_prediction_dnn.joblib) do (
    if exist "%%A" (
        echo   ✓ %%A
    ) else (
        echo   ✗ %%A (missing)
        set /a MISSING_MODELS=!MISSING_MODELS!+1
    )
)

if !MISSING_MODELS! gtr 0 (
    echo.
    echo ⚠ Warning: !MISSING_MODELS! model(s) missing
    echo   The API will work with available models only
)

echo.
echo [*] Starting FastAPI server...
echo     Host: 0.0.0.0
echo     Port: 8000
echo     API Docs: http://localhost:8000/docs
echo     ReDoc: http://localhost:8000/redoc
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

if errorlevel 1 (
    echo ❌ Failed to start server
    pause
    exit /b 1
)

pause
