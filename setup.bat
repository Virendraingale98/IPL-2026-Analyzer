@echo off
REM IPL 2026 Full Stack Setup - Windows Batch Script

echo.
echo ========================================
echo   IPL 2026 - Full Stack Setup
echo ========================================
echo.

REM Backend Setup
echo [1/2] Setting up Backend (Flask)...
cd /d "g:\My Drive\Projects\AI_Mastery_Roadmap\scratch\ipl-2026\backend"

echo Clearing pip cache...
pip cache purge

echo Installing Python packages...
pip install -r requirements.txt

echo Seeding database...
python seed_data.py

echo.
echo [2/2] Setting up Frontend (React)...
cd /d "g:\My Drive\Projects\AI_Mastery_Roadmap\scratch\ipl-2026\frontend"

echo Clearing npm cache...
call npm cache clean --force

if exist node_modules rmdir /s /q node_modules
if exist package-lock.json del package-lock.json

echo Installing Node packages...
call npm install

echo.
echo ========================================
echo   ✓ Setup Complete!
echo ========================================
echo.
echo Start your app:
echo.
echo Terminal 1 (Backend):
echo   cd backend
echo   python app.py
echo.
echo Terminal 2 (Frontend):
echo   cd frontend
echo   npm run dev
echo.
echo Then open: http://localhost:5173
echo.
pause
