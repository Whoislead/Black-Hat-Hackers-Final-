@echo off
echo Starting Evil Twin Detection API Server...

REM Check if virtual environment exists
if not exist venv (
    echo Virtual environment not found. Please run setup.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Start the server
echo.
echo ========================================
echo Starting FastAPI Server...
echo ========================================
echo.
echo Server will be available at:
echo - Main API: http://localhost:8000
echo - Documentation: http://localhost:8000/docs
echo - Interactive API: http://localhost:8000/redoc
echo.
echo Press Ctrl+C to stop the server
echo.

python main.py
