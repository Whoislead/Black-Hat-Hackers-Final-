@echo off
echo Installing Evil Twin Detection API Server...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Check if we're in a virtual environment, if not create one
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Check if installation was successful
if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ========================================
echo Evil Twin Detection API Server Setup Complete!
echo ========================================
echo.
echo To start the server, run: start_server.bat
echo Or manually run: python main.py
echo.
echo The API will be available at: http://localhost:8000
echo API documentation at: http://localhost:8000/docs
echo.
pause
