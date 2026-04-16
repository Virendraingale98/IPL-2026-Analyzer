# IPL 2026 Real-Time Cricket Board 🏏

A full-stack web application for IPL 2026 with real-time live scores, standings, match schedules, player information, and ball-by-ball commentary.

## Features

✅ **Live Score Updates** - Real-time match scores with WebSocket support  
✅ **Match Schedule** - Complete fixture list with upcoming matches  
✅ **Team Standings** - Current IPL standings with points table  
✅ **Player Statistics** - Player info, performance metrics, and team rosters  
✅ **Ball-by-Ball Commentary** - Live commentary and match updates  
✅ **Responsive Design** - Works on desktop, tablet, and mobile  
✅ **Real-time Notifications** - WebSocket-based instant updates  

## Tech Stack

### Backend
- **Flask** - Python web framework
- **Flask-SQLAlchemy** - ORM for database management
- **Flask-SocketIO** - WebSocket support for real-time updates
- **SQLite** - Lightweight database

### Frontend
- **React** - UI library
- **TypeScript** - Type-safe JavaScript
- **Socket.IO** - Real-time communication
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client

## Project Structure

```
ipl-2026/
├── backend/
│   ├── app.py              # Main Flask app
│   ├── models.py           # Database models
│   ├── seed_data.py        # Sample data seeder
│   └── requirements.txt     # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── App.tsx         # Main App component
│   │   ├── main.tsx        # Entry point
│   │   └── App.css         # Global styles
│   ├── public/
│   │   └── index.html      # HTML template
│   └── package.json        # Frontend dependencies
│
└── README.md               # This file
```

## Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 16+ & npm
- Flask, Flask-SocketIO

### Backend Setup

1. Navigate to backend directory:
```bash
cd ipl-2026/backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Seed the database with sample data:
```bash
python seed_data.py
```

4. Run Flask server:
```bash
python app.py
```

The backend will run on `http://localhost:5000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd ../frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm run dev
```

The frontend will run on `http://localhost:5173` (Vite default)

## API Endpoints

### Teams
- `GET /api/teams` - Get all teams
- `POST /api/teams` - Create new team
- `GET /api/teams/<id>` - Get team details with players

### Matches
- `GET /api/matches` - Get all matches
- `GET /api/matches?status=Live` - Get live matches
- `POST /api/matches` - Create new match
- `GET /api/matches/<id>` - Get match details
- `PATCH /api/matches/<id>/update` - Update match score
- `POST /api/matches/<id>/commentary` - Add commentary

### Players
- `GET /api/players` - Get all players
- `GET /api/players?team_id=1` - Get team players
- `GET /api/players?role=Batsman` - Get players by role
- `POST /api/players` - Create new player

### Standings
- `GET /api/standings` - Get points table

### Health
- `GET /health` - Server health check

## WebSocket Events

### Client to Server
- `join_match` - Join a match room for live updates
- `leave_match` - Leave a match room

### Server to Client
- `connection_response` - Connection confirmation
- `match_update` - Live score update
- `match_created` - New match created
- `new_commentary` - Ball-by-ball commentary

## Database Schema

### Teams Table
- `id` - Primary key
- `name` - Team name
- `logo_url` - Team logo
- `home_ground` - Home stadium
- `wins`, `losses`, `matches_played`, `points` - Statistics

### Players Table
- `id` - Primary key
- `name` - Player name
- `team_id` - Team reference
- `role` - Batsman/Bowler/All-rounder
- `jersey_number` - Jersey #
- `runs_scored`, `wickets_taken`, `matches_played` - Stats

### Matches Table
- `id` - Primary key
- `match_number` - Match #
- `home_team_id`, `away_team_id` - Team references
- `status` - Scheduled/Live/Completed
- `scores`, `wickets`, `overs_completed` - Match data
- `result`, `man_of_match`, `toss_info` - Match details

### Commentary Table
- `id` - Primary key
- `match_id` - Match reference
- `ball_number` - Over.Ball (e.g., 5.3)
- `batsman`, `bowler` - Player names
- `description` - Ball outcome
- `runs`, `is_wicket` - Ball data

## Usage Examples

### Starting a Match
```bash
curl -X PATCH http://localhost:5000/api/matches/1/update \
  -H "Content-Type: application/json" \
  -d '{
    "status": "Live",
    "home_team_score": 45,
    "home_team_wickets": 2,
    "overs_completed": 5.3
  }'
```

### Adding Commentary
```bash
curl -X POST http://localhost:5000/api/matches/1/commentary \
  -H "Content-Type: application/json" \
  -d '{
    "ball_number": 5.3,
    "batsman": "Rohit Sharma",
    "bowler": "Jasprit Bumrah",
    "runs": 4,
    "description": "Four!"
  }'
```

## Future Enhancements

🔄 **Planned Features:**
- Player auction simulator
- Fantasy cricket league
- Match predictions using machine learning
- Push notifications
- Mobile app (React Native)
- Admin dashboard for live updates
- Advanced statistics & analytics
- Video highlights integration
- User authentication & profiles
- Betting odds integration

## Running the Full Stack

### Terminal 1 - Backend
```bash
cd ipl-2026/backend
python app.py
```

### Terminal 2 - Frontend
```bash
cd ipl-2026/frontend
npm run dev
```

Then open browser to `http://localhost:5173`

## Troubleshooting

**CORS Errors?**
- Backend CORS is enabled for `*`. Ensure frontend URL matches.

**WebSocket Connection Fails?**
- Check backend is running on port 5000
- Ensure you're using `http://` not `https://`

**Database Issues?**
- Delete `ipl_2026.db` and run `python seed_data.py` again

**Port Already in Use?**
- Backend: Change port in `app.py` - `socketio.run(..., port=5001)`
- Frontend: Change port in Vite config

## Contributing

Contributions welcome! Fork the repo and submit PRs.

## License

MIT License - See LICENSE file for details

---

**Built with ❤️ for IPL 2026** 🏏
