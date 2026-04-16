@echo off
echo Installing IPL 2026 Frontend...
echo.

cd /d "g:\My Drive\Projects\AI_Mastery_Roadmap\scratch\ipl-2026\frontend"

echo Clearing npm cache...
call npm cache clean --force

echo Removing old node_modules...
if exist node_modules rmdir /s /q node_modules
if exist package-lock.json del package-lock.json

echo Installing dependencies...
call npm install

echo.
echo ✓ Installation complete!
echo Starting dev server...
call npm run dev
