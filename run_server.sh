#!/bin/bash

# ViralLens AI - FastAPI Server Startup Script
# This script starts the FastAPI server with optimal settings

set -e  # Exit on error

echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║                   ViralLens AI - FastAPI Server                             ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Check if requirements are installed
echo "[*] Checking dependencies..."
python -c "import fastapi" 2>/dev/null || {
    echo "❌ FastAPI not installed"
    echo "[*] Installing dependencies..."
    pip install -r requirements.txt
}

# Check if models exist
echo "[*] Checking for trained models..."
MODELS=("logistic_regression_pipeline.joblib" "random_forest_pipeline.joblib" "xgboost_pipeline.joblib" "viral_prediction_dnn.joblib")
MISSING_MODELS=0

for model in "${MODELS[@]}"; do
    if [ -f "$model" ]; then
        echo "  ✓ $model"
    else
        echo "  ✗ $model (missing)"
        MISSING_MODELS=$((MISSING_MODELS + 1))
    fi
done

if [ $MISSING_MODELS -gt 0 ]; then
    echo ""
    echo "⚠ Warning: $MISSING_MODELS model(s) missing"
    echo "  The API will work with available models only"
fi

echo ""
echo "[*] Starting FastAPI server..."
echo "    Host: 0.0.0.0"
echo "    Port: 8000"
echo "    API Docs: http://localhost:8000/docs"
echo "    ReDoc: http://localhost:8000/redoc"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
# Use --reload for development, remove it for production
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
