#!/bin/bash
# Simple Flask app stopper script

echo "Stopping Flask Task Manager..."

# Kill Flask processes
pkill -f "python.*app.py" && echo "✅ Flask app stopped" || echo "ℹ️ No Flask app running"

# Remove PID file if exists
rm -f flask.pid

echo "Flask app stopped successfully"