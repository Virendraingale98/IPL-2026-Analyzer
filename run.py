import os
import subprocess
import sys
import time

print("\n🏏 IPL 2026 Real-time Cricket Board")
print("=" * 40)
print()

# Backend setup
print("Starting Backend (Flask)...")
os.chdir('backend')

# Install dependencies
print("Installing backend dependencies...")
os.system(f"{sys.executable} -m pip install -r requirements.txt")

# Seed database
print("Seeding database...")
os.system(f"{sys.executable} seed_data.py")

# Start backend
print("Starting Flask server...")
backend_process = subprocess.Popen([sys.executable, 'app.py'])
time.sleep(3)

# Frontend setup
print("\nStarting Frontend (React)...")
os.chdir('../frontend')

# Install dependencies
print("Installing frontend dependencies...")
os.system("npm install")

# Start frontend
print("Starting React dev server...")
frontend_process = subprocess.Popen(['npm', 'run', 'dev'])

print("\n✅ Servers started!")
print("- Backend:  http://localhost:5000")
print("- Frontend: http://localhost:5173")
print("\nPress Ctrl+C to stop both servers\n")

try:
    backend_process.wait()
    frontend_process.wait()
except KeyboardInterrupt:
    print("\n\nShutting down...")
    backend_process.terminate()
    frontend_process.terminate()
    print("✓ Servers stopped")
