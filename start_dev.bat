@echo off
echo 🔧 Starting RAG Development Server with Auto-Reload
echo =====================================================
echo.

REM Change to script directory
cd /d "%~dp0"

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo 🐍 Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo ⚠️  No virtual environment found. Using system Python.
)

REM Install dependencies if needed
echo 📦 Checking dependencies...
python -c "import watchdog" >nul 2>&1 || (
    echo 📦 Installing watchdog for auto-reload...
    pip install watchdog
)

REM Start development server
echo.
echo 🚀 Starting development server...
echo 🔄 Auto-reload enabled - server will restart when code changes
echo ⌨️  Press Ctrl+C to stop
echo.
python run_dev.py

pause
