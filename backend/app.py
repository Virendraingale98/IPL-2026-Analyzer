from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room, leave_room
from models import db, Team, Player, Match, Commentary
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ipl_2026.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')

db.init_app(app)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize database once at startup
with app.app_context():
    db.create_all()

# ==================== TEAMS API ====================
@app.route('/api/teams', methods=['GET'])
def get_teams():
    """Get all teams sorted by points"""
    teams = Team.query.order_by(Team.points.desc()).all()
    return jsonify([team.to_dict() for team in teams])

@app.route('/api/teams', methods=['POST'])
def create_team():
    """Create a new team"""
    data = request.json
    team = Team(
        name=data['name'],
        logo_url=data.get('logo_url'),
        home_ground=data.get('home_ground')
    )
    db.session.add(team)
    db.session.commit()
    return jsonify(team.to_dict()), 201

@app.route('/api/teams/<int:team_id>', methods=['GET'])
def get_team(team_id):
    """Get team details with players"""
    team = Team.query.get_or_404(team_id)
    team_data = team.to_dict()
    team_data['players'] = [player.to_dict() for player in team.players]
    return jsonify(team_data)

# ==================== MATCHES API ====================
@app.route('/api/matches', methods=['GET'])
def get_matches():
    """Get all matches with filters"""
    status = request.args.get('status')
    query = Match.query
    
    if status:
        query = query.filter_by(status=status)
    
    matches = query.order_by(Match.scheduled_date).all()
    return jsonify([match.to_dict() for match in matches])

@app.route('/api/matches', methods=['POST'])
def create_match():
    """Create a new match"""
    data = request.json
    match = Match(
        match_number=data['match_number'],
        home_team_id=data['home_team_id'],
        away_team_id=data['away_team_id'],
        venue=data.get('venue'),
        scheduled_date=datetime.fromisoformat(data['scheduled_date'])
    )
    db.session.add(match)
    db.session.commit()
    
    socketio.emit('match_created', match.to_dict(), broadcast=True)
    return jsonify(match.to_dict()), 201

@app.route('/api/matches/<int:match_id>', methods=['GET'])
def get_match(match_id):
    """Get match details with commentary"""
    match = Match.query.get_or_404(match_id)
    match_data = match.to_dict()
    match_data['commentary'] = [c.to_dict() for c in match.commentary_entries]
    return jsonify(match_data)

@app.route('/api/matches/<int:match_id>/update', methods=['PATCH'])
def update_match(match_id):
    """Update match score and status (for live updates)"""
    match = Match.query.get_or_404(match_id)
    data = request.json
    
    if 'status' in data:
        match.status = data['status']
    if 'home_team_score' in data:
        match.home_team_score = data['home_team_score']
    if 'away_team_score' in data:
        match.away_team_score = data['away_team_score']
    if 'home_team_wickets' in data:
        match.home_team_wickets = data['home_team_wickets']
    if 'away_team_wickets' in data:
        match.away_team_wickets = data['away_team_wickets']
    if 'overs_completed' in data:
        match.overs_completed = data['overs_completed']
    if 'result' in data:
        match.result = data['result']
    if 'man_of_match' in data:
        match.man_of_match = data['man_of_match']
    
    match.updated_at = datetime.utcnow()
    db.session.commit()
    
    # Broadcast live update via WebSocket
    socketio.emit('match_update', match.to_dict(), broadcast=True)
    
    return jsonify(match.to_dict())

@app.route('/api/matches/<int:match_id>/commentary', methods=['POST'])
def add_commentary(match_id):
    """Add commentary/ball update for a match"""
    match = Match.query.get_or_404(match_id)
    data = request.json
    
    commentary = Commentary(
        match_id=match_id,
        ball_number=data['ball_number'],
        batsman=data.get('batsman'),
        bowler=data.get('bowler'),
        description=data.get('description'),
        runs=data.get('runs', 0),
        is_wicket=data.get('is_wicket', False)
    )
    db.session.add(commentary)
    db.session.commit()
    
    # Broadcast commentary via WebSocket
    socketio.emit('new_commentary', {
        'match_id': match_id,
        'commentary': commentary.to_dict()
    }, broadcast=True)
    
    return jsonify(commentary.to_dict()), 201

# ==================== STANDINGS API ====================
@app.route('/api/standings', methods=['GET'])
def get_standings():
    """Get IPL standings"""
    teams = Team.query.order_by(Team.points.desc()).all()
    standings = []
    for rank, team in enumerate(teams, 1):
        team_data = team.to_dict()
        team_data['rank'] = rank
        standings.append(team_data)
    return jsonify(standings)

# ==================== PLAYERS API ====================
@app.route('/api/players', methods=['GET'])
def get_players():
    """Get all players with filters"""
    team_id = request.args.get('team_id')
    role = request.args.get('role')
    query = Player.query
    
    if team_id:
        query = query.filter_by(team_id=team_id)
    if role:
        query = query.filter_by(role=role)
    
    players = query.all()
    return jsonify([player.to_dict() for player in players])

@app.route('/api/players', methods=['POST'])
def create_player():
    """Create a new player"""
    data = request.json
    player = Player(
        name=data['name'],
        team_id=data['team_id'],
        role=data.get('role'),
        jersey_number=data.get('jersey_number')
    )
    db.session.add(player)
    db.session.commit()
    return jsonify(player.to_dict()), 201

@app.route('/api/players/<int:player_id>', methods=['GET'])
def get_player(player_id):
    """Get player details"""
    player = Player.query.get_or_404(player_id)
    return jsonify(player.to_dict())

# ==================== WEBSOCKET EVENTS ====================
@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('connection_response', {'data': 'Connected to IPL 2026 Live Server'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('join_match')
def on_join_match(data):
    """Join a match room for live updates"""
    match_id = data['match_id']
    join_room(f'match_{match_id}')
    emit('joined_match', {'match_id': match_id})

@socketio.on('leave_match')
def on_leave_match(data):
    """Leave a match room"""
    match_id = data['match_id']
    leave_room(f'match_{match_id}')
    emit('left_match', {'match_id': match_id})

# ==================== HEALTH CHECK ====================
@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, debug=False, host='0.0.0.0', port=port)
