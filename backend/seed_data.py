from app import app, db
from models import Team, Player, Match
from datetime import datetime, timedelta

def seed_ipl_2026():
    """Seed initial IPL 2026 data"""
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()
        
        # IPL 2026 Teams
        teams_data = [
            {'name': 'Mumbai Indians', 'home_ground': 'Wankhede Stadium'},
            {'name': 'Chennai Super Kings', 'home_ground': 'M. A. Chidambaram Stadium'},
            {'name': 'Delhi Capitals', 'home_ground': 'Arun Jaitley Stadium'},
            {'name': 'Royal Challengers Bangalore', 'home_ground': 'M. Chinnaswamy Stadium'},
            {'name': 'Kolkata Knight Riders', 'home_ground': 'Eden Gardens'},
            {'name': 'Sun Risers Hyderabad', 'home_ground': 'Rajiv Gandhi Intl Cricket Stadium'},
            {'name': 'Rajasthan Royals', 'home_ground': 'Sawai Mansingh Stadium'},
            {'name': 'Punjab Kings', 'home_ground': 'PCA Stadium'},
            {'name': 'Lucknow Super Giants', 'home_ground': 'ARUN Jaitley Stadium'},
            {'name': 'Gujarat Titans', 'home_ground': 'Narendra Modi Stadium'},
        ]
        
        teams = []
        for team_data in teams_data:
            team = Team(
                name=team_data['name'],
                home_ground=team_data['home_ground'],
                points=0,
                matches_played=0,
                wins=0,
                losses=0
            )
            teams.append(team)
            db.session.add(team)
        
        db.session.commit()
        
        # Sample Players (2-3 per team for demo)
        players_data = [
            # Mumbai Indians
            {'team_id': 1, 'name': 'Rohit Sharma', 'role': 'Batsman', 'jersey': 45},
            {'team_id': 1, 'name': 'Jasprit Bumrah', 'role': 'Bowler', 'jersey': 93},
            {'team_id': 1, 'name': 'Suryakumar Yadav', 'role': 'Batsman', 'jersey': 63},
            
            # Chennai Super Kings
            {'team_id': 2, 'name': 'MS Dhoni', 'role': 'Batsman', 'jersey': 7},
            {'team_id': 2, 'name': 'Ravindra Jadeja', 'role': 'All-rounder', 'jersey': 8},
            {'team_id': 2, 'name': 'Ruturaj Gaikwad', 'role': 'Batsman', 'jersey': 31},
            
            # Delhi Capitals
            {'team_id': 3, 'name': 'Rishabh Pant', 'role': 'Batsman', 'jersey': 17},
            {'team_id': 3, 'name': 'Axar Patel', 'role': 'All-rounder', 'jersey': 12},
            {'team_id': 3, 'name': 'David Warner', 'role': 'Batsman', 'jersey': 1},
        ]
        
        for player_data in players_data:
            player = Player(
                team_id=player_data['team_id'],
                name=player_data['name'],
                role=player_data['role'],
                jersey_number=player_data['jersey']
            )
            db.session.add(player)
        
        db.session.commit()
        
        # Sample Matches
        base_date = datetime.now() + timedelta(days=1)
        matches_data = [
            {'match_num': 1, 'home': 1, 'away': 2, 'venue': 'Wankhede Stadium'},
            {'match_num': 2, 'home': 3, 'away': 4, 'venue': 'Arun Jaitley Stadium'},
            {'match_num': 3, 'home': 5, 'away': 6, 'venue': 'Eden Gardens'},
            {'match_num': 4, 'home': 7, 'away': 8, 'venue': 'Sawai Mansingh Stadium'},
            {'match_num': 5, 'home': 9, 'away': 10, 'venue': 'Arun Jaitley Stadium'},
        ]
        
        for i, match_data in enumerate(matches_data):
            match = Match(
                match_number=match_data['match_num'],
                home_team_id=match_data['home'],
                away_team_id=match_data['away'],
                venue=match_data['venue'],
                scheduled_date=base_date + timedelta(days=i),
                status='Scheduled'
            )
            db.session.add(match)
        
        db.session.commit()
        print("✅ IPL 2026 database seeded successfully!")

if __name__ == '__main__':
    seed_ipl_2026()
