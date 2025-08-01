#!/bin/bash
# Simple Flask app starter script

# Kill existing processes
pkill -f "python.*app.py" || true

# Start Flask app
echo "Starting Flask Task Manager on port 5000..."
nohup python3 app.py > app.log 2>&1 &

# Get the process ID
FLASK_PID=$!
echo "Flask app started with PID: $FLASK_PID"
echo $FLASK_PID > flask.pid

# Wait and verify
sleep 2
if pgrep -f "python.*app.py" > /dev/null; then
    echo "✅ Flask app is running on http://0.0.0.0:5000"
else
    echo "❌ Failed to start Flask app"
    exit 1
fi