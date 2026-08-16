# start_backend.ps1
# This script activates the virtual environment and starts the Waitress WSGI server on port 8001.

# Ensure we run from the script's directory
$ScriptDir = Split-Path $MyInvocation.MyCommand.Path
$BackendDir = Join-Path (Split-Path $ScriptDir) "backend"

Set-Location $BackendDir

Write-Host "Starting NuruX Backend with Waitress on port 8001..." -ForegroundColor Green

# Activate virtual environment
if (Test-Path ".\venv\Scripts\Activate.ps1") {
    .\venv\Scripts\Activate.ps1
} else {
    Write-Host "Virtual environment not found! Please run 'python -m venv venv' and install requirements." -ForegroundColor Red
    Pause
    exit
}

# Run Waitress
waitress-serve --listen=127.0.0.1:8001 --threads=4 config.wsgi:application
