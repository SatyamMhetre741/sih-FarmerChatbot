#!/bin/bash
echo "Starting AI Farmer Query Support System..."
echo

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo
    echo "⚠️  WARNING: .env file not found!"
    echo "Please copy .env.example to .env and add your API keys:"
    echo
    echo "  cp .env.example .env"
    echo
    echo "Then edit .env file and add your Gemini API key."
    echo
    read -p "Press Enter to continue..."
    exit 1
fi

# Start the server
echo
echo "🚀 Starting FastAPI server..."
echo "Access the API at: http://localhost:8000"
echo "API documentation at: http://localhost:8000/docs"
echo
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000