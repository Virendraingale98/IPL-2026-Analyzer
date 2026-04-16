@echo off
REM IPL 2026 Full Stack Runner for Windows
REM This script starts both backend and frontend servers

echo.
echo iPL 2026 Real-time Cricket Board
echo ====================================
echo.

REM Start Backend
echo Starting Backend (Flask)...
cd backend
python -m pip install -q -r requirements.txt 2>nul
python seed_data.py
start "IPL 2026 Backend" python app.py
timeout /t 2 /nobreak

REM Start Frontend
echo Starting Frontend (React)...
cd ../frontend
call npm install --quiet 2>nul
start "IPL 2026 Frontend" npm run dev

echo.
echo ✓ Servers started!
echo - Backend:  http://localhost:5000
echo - Frontend: http://localhost:5173
echo.
echo Press Ctrl+C in each window to stop servers
pause
