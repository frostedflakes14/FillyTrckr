#!/bin/bash

echo "Starting FillyTrckr Frontend and Backend..."
echo ""

# Start the backend in the background
echo "Starting Backend (Python)..."
python backend/main.py &
BACKEND_PID=$!

# Start the frontend in the background
echo "Starting Frontend (npm)..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "Both services are running in the background..."
echo "Backend: http://localhost:8000 (PID: $BACKEND_PID)"
echo "Frontend: http://localhost:5173 (PID: $FRONTEND_PID)"
echo ""
echo "Press Ctrl+C to stop all services..."

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "Stopping services..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "Services stopped."
    exit 0
}

# Trap Ctrl+C and call cleanup
trap cleanup SIGINT SIGTERM

# Wait for both processes
wait
