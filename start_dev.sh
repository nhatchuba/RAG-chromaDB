#!/bin/bash

echo "🔧 Starting RAG Development Server with Auto-Reload"
echo "====================================================="
echo

# Change to script directory
cd "$(dirname "$0")"

# Check if virtual environment exists
if [ -f "venv/bin/activate" ]; then
    echo "🐍 Activating virtual environment..."
    source venv/bin/activate
else
    echo "⚠️  No virtual environment found. Using system Python."
fi

# Install dependencies if needed
echo "📦 Checking dependencies..."
python -c "import watchdog" 2>/dev/null || {
    echo "📦 Installing watchdog for auto-reload..."
    pip install watchdog
}

# Start development server
echo
echo "🚀 Starting development server..."
echo "🔄 Auto-reload enabled - server will restart when code changes"
echo "⌨️  Press Ctrl+C to stop"
echo
python run_dev.py
