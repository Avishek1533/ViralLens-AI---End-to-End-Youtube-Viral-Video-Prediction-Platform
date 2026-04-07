#!/bin/bash

# ViralLens AI - Example Usage Script
# This script runs the example_usage.py with proper error handling

set -e  # Exit on error

echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║        ViralLens AI - FastAPI Examples & API Testing                       ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Check if the API is running
echo "[*] Checking if API server is running..."
if ! curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "❌ API server is not running at http://localhost:8000"
    echo ""
    echo "Please start the API server first using:"
    echo "  ./run_server.sh"
    echo "or"
    echo "  uvicorn main:app --reload"
    exit 1
fi

echo "✓ API server is up and running!"
echo ""

# Check if requests library is installed
echo "[*] Checking dependencies..."
python -c "import requests" 2>/dev/null || {
    echo "❌ Requests library not installed"
    echo "[*] Installing..."
    pip install requests
}

echo ""
echo "[*] Running examples..."
echo ""

# Run examples
python example_usage.py

echo ""
echo "Examples completed successfully!"
echo ""
echo "For more information, check:"
echo "  • API Documentation: http://localhost:8000/docs"
echo "  • README: README.md"
echo "  • API Guide: API_GUIDE.md"
echo ""
