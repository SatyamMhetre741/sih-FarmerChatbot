@echo off
echo Starting AI Farmer Query Support System...
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Check if .env exists
if not exist ".env" (
    echo.
    echo ⚠️  WARNING: .env file not found!
    echo Please copy .env.example to .env and add your API keys:
    echo.
    echo   copy .env.example .env
    echo.
    echo Then edit .env file and add your Gemini API key.
    echo.
    pause
    exit /b 1
)

REM Start the server
echo.
echo 🚀 Starting FastAPI server...
echo Access the API at: http://localhost:8000
echo API documentation at: http://localhost:8000/docs
echo.
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000