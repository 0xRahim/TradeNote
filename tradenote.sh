#!/usr/bin/env bash
set -euo pipefail

# Kill background children on exit
cleanup() {
  echo "Stopping servers..."
  pkill -P $$ || true    # kill child processes of this script
}
trap cleanup EXIT

# Start backend (adjust command if different)
echo "Starting backend server..."
(
  cd backend || { echo "backend directory missing"; exit 1; }
  source venv/bin/activate
  python run.py
) > backend.log 2>&1 & 
BACKEND_PID=$!

# Start frontend on port 1111 (change to 8080 if you prefer)
FRONTEND_PORT=1111
echo "Starting frontend server on port ${FRONTEND_PORT}..."
python3 -m http.server "${FRONTEND_PORT}" --directory frontend > frontend.log 2>&1 &
FRONTEND_PID=$!

FRONTEND_URL="http://localhost:${FRONTEND_PORT}/index.html"

echo
echo "======================================================"
echo "  TradeNote Application Started"
echo "======================================================"
echo "Backend PID: ${BACKEND_PID} (logs: backend.log)"
echo "Frontend PID: ${FRONTEND_PID} (logs: frontend.log)"
echo "Frontend is served at: ${FRONTEND_URL}"
echo

read -p "Press [Enter] to open the application in your browser..."
xdg-open "$FRONTEND_URL" || echo "xdg-open failed (maybe no GUI)"

# Wait for background processes (this waits for both; will only exit when both exit)
wait "${BACKEND_PID}" "${FRONTEND_PID}"
