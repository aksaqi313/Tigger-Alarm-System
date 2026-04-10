# Water Level Alarm System - Quick Start (PowerShell)
# Run this script to set up and start the Flask application

Write-Host ""
Write-Host "============================================================"
Write-Host "  Water Level Alarm System - Python Flask Application"
Write-Host "============================================================"
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[✓] Python found: $pythonVersion"
} catch {
    Write-Host "[✗] ERROR: Python is not installed or not in PATH"
    Write-Host "    Please install Python from https://www.python.org/"
    Write-Host "    Make sure to check 'Add Python to PATH' during installation"
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[1/4] Checking for virtual environment..."
if (-not (Test-Path "venv")) {
    Write-Host "[2/4] Creating virtual environment..."
    & python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[✗] ERROR: Failed to create virtual environment"
        Read-Host "Press Enter to exit"
        exit 1
    }
}

Write-Host "[3/4] Activating virtual environment and installing dependencies..."
& ".\venv\Scripts\Activate.ps1"
& pip install -q -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "[✗] ERROR: Failed to install dependencies"
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[4/4] Starting Flask application..."
Write-Host ""
Write-Host "============================================================"
Write-Host "  Server starting... Open http://localhost:5000 in browser"
Write-Host "============================================================"
Write-Host ""

# Try to open browser
Start-Process "http://localhost:5000"

# Run Flask app
& python app.py
