@echo off
REM Water Level Alarm System - Quick Start for Windows
REM This script sets up and runs the Flask application

echo.
echo ============================================================
echo   Water Level Alarm System - Python Flask Application
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [1/4] Python found. Checking for virtual environment...
if not exist "venv" (
    echo [2/4] Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
)

echo [3/4] Activating virtual environment and installing dependencies...
call venv\Scripts\activate.bat
pip install -q -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo [4/4] Starting Flask application...
echo.
echo ============================================================
echo   Server starting... Opening browser in 2 seconds
echo ============================================================
echo.

timeout /t 2 /nobreak

REM Try to open browser
start http://localhost:5000

REM Run Flask app
python app.py
