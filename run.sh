#!/bin/bash

# IPL 2026 Full Stack Runner
# This script starts both backend and frontend servers

echo "🏏 IPL 2026 Real-time Cricket Board"
echo "===================================="

# Colors
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Start Backend
echo -e "${GREEN}Starting Backend (Flask)...${NC}"
cd backend
python -m pip install -q -r requirements.txt 2>/dev/null || echo "Dependencies already installed"
python seed_data.py
python app.py &
BACKEND_PID=$!
sleep 2

# Start Frontend
echo -e "${GREEN}Starting Frontend (React)...${NC}"
cd ../frontend
npm install -q 2>/dev/null || echo "Dependencies already installed"
npm run dev &
FRONTEND_PID=$!

echo ""
echo -e "${GREEN}✅ Servers started!${NC}"
echo "- Backend:  http://localhost:5000"
echo "- Frontend: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for processes
wait $BACKEND_PID $FRONTEND_PID
