# IPL 2026 - Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Option 1: One-Command Start (Easiest)

**Windows:**
```bash
cd ipl-2026
python run.py
```

**macOS/Linux:**
```bash
cd ipl-2026
bash run.sh
```

Open browser to: `http://localhost:5173`

---

### Option 2: Manual Setup

**Terminal 1 - Backend:**
```bash
cd ipl-2026/backend
pip install -r requirements.txt
python seed_data.py      # Seed sample data
python app.py            # Start Flask server
```

**Terminal 2 - Frontend:**
```bash
cd ipl-2026/frontend
npm install              # Install dependencies
npm run dev              # Start Vite dev server
```

Then open: `http://localhost:5173` in your browser

---

## 📋 What You'll See

1. **Dashboard** - Live match stats and quick overview
2. **Standings** - Teams ranked by points
3. **Matches** - Upcoming, live, and completed matches
4. **Players** - Browse players by team/role

---

## 🔄 Real-Time Features

- **Live Scores** - Scores update instantly via WebSocket
- **Match Status** - See who's playing and current scores
- **Commentary** - Ball-by-ball updates (when match is live)

---

## 🎮 Testing Live Updates

### Using curl to simulate live updates:

```bash
# Start a match
curl -X PATCH http://localhost:5000/api/matches/1/update \
  -H "Content-Type: application/json" \
  -d '{"status": "Live", "home_team_score": 45, "home_team_wickets": 2, "overs_completed": 5.3}'

# Add commentary
curl -X POST http://localhost:5000/api/matches/1/commentary \
  -H "Content-Type: application/json" \
  -d '{
    "ball_number": 5.3,
    "batsman": "Rohit Sharma",
    "bowler": "Jasprit Bumrah",
    "runs": 4,
    "description": "Four at long off!"
  }'

# Update final score
curl -X PATCH http://localhost:5000/api/matches/1/update \
  -H "Content-Type: application/json" \
  -d '{
    "status": "Completed",
    "result": "Mumbai Indians won by 8 runs",
    "man_of_match": "Rohit Sharma"
  }'
```

---

## 📁 Project Structure

```
ipl-2026/
├── backend/          # Flask API + Database
├── frontend/         # React UI
├── README.md         # Full documentation
├── run.py            # Python runner script
├── run.sh            # Bash runner script
├── run.bat           # Windows runner script
└── QUICKSTART.md     # This file
```

---

## 🐛 Troubleshooting

### Backend won't start?
```bash
# Check Python version (need 3.8+)
python --version

# Try installing deps manually
cd backend
pip install -r requirements.txt
```

### Frontend won't start?
```bash
# Check Node version (need 16+)
node --version

# Clear cache and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Port already in use?
- Backend (5000): Edit `backend/app.py` line with `socketio.run(..., port=5001)`
- Frontend (5173): Edit `frontend/vite.config.ts` to use different port

### WebSocket not connecting?
- Ensure backend is running first
- Check browser console for errors
- Firewall might be blocking port 5000

---

## 📚 API Quick Reference

### Get all teams:
```bash
curl http://localhost:5000/api/teams
```

### Get live matches:
```bash
curl http://localhost:5000/api/matches?status=Live
```

### Get standings:
```bash
curl http://localhost:5000/api/standings
```

---

## 🎯 Next Steps

1. ✅ Start the servers (using one of the methods above)
2. 🌐 Open http://localhost:5173 in browser
3. 🏏 Explore the dashboard
4. 🔄 Simulate live matches using curl commands
5. 📊 Customize and extend features

---

## 💡 Features to Try

- Filter matches by status
- Sort standings by points
- Search players by role
- Watch real-time score updates
- Add ball-by-ball commentary

---

**Need help?** Check [README.md](./README.md) for complete documentation!

🏏 Enjoy the IPL 2026 experience!
