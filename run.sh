#!/bin/bash

# PGP Tool Launcher Script

echo "🔐 Starting PGP Tool..."

# Activate virtual environment
source venv/bin/activate

# Check if GnuPG is installed
if ! command -v gpg &> /dev/null; then
    echo "❌ Error: GnuPG is not installed"
    echo "Install with: brew install gnupg"
    exit 1
fi

# Create necessary directories
mkdir -p data keys
chmod 700 data keys

echo "✅ Environment ready"
echo "🚀 Starting Flask server..."
echo "📍 Open your browser at: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run the Flask application
python app.py
