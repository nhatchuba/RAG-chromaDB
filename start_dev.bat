@echo off
chcp 65001 >nul
echo [DEV] Starting RAG Development Server with Auto-Reload
echo =====================================================
echo.

REM Change to script directory
cd /d "%~dp0"

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo [PYTHON] Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo [WARNING] No virtual environment found. Using system Python.
)

REM Install dependencies if needed
echo [PACKAGE] Checking dependencies...
python -c "import watchdog" >nul 2>&1 || (
    echo [PACKAGE] Installing watchdog for auto-reload...
    pip install watchdog
)

REM Start development server
echo.
echo [START] Starting development server...
echo [AUTO] Auto-reload enabled - server will restart when code changes
echo [CTRL+C] Press Ctrl+C to stop
echo.
python run_dev.py

pause
