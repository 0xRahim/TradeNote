#!/bin/bash

# Function to clean up background processes on exit
cleanup() {
    echo "Stopping servers..."
    # Kill all processes in the same process group as the script
    kill 0
}

# Trap the EXIT signal to run the cleanup function
trap cleanup EXIT

# Activate virtual environment and start backend API server in the background
echo "Starting backend server..."
(cd backend && source venv/bin/activate && python run.py) &

# Start frontend server in the background
echo "Starting frontend server on port 8080..."
python3 -m http.server 8080 --directory frontend &

# Define the frontend URL
FRONTEND_URL="http://localhost:1111/index.html"

# Output information to the user
echo
echo "======================================================"
echo "  TradeNote Application Started"
echo "======================================================"
echo
echo "Backend API server is running."
echo "Frontend is served at: $FRONTEND_URL"
echo

# Prompt the user to open the URL
read -p "Press [Enter] to open the application in your browser..."

# Open the URL in the default browser
xdg-open "$FRONTEND_URL"

# Wait indefinitely to keep the script and background servers running
# The user can stop everything by closing the terminal or pressing Ctrl+C
wait
