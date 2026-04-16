from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Float, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List, Optional

db = SQLAlchemy()

class Team(db.Model):
    __tablename__ = 'teams'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    logo_url: Mapped[Optional[str]] = mapped_column(String(500))
    home_ground: Mapped[Optional[str]] = mapped_column(String(100))
    wins: Mapped[int] = mapped_column(Integer, default=0)
    losses: Mapped[int] = mapped_column(Integer, default=0)
    matches_played: Mapped[int] = mapped_column(Integer, default=0)
    points: Mapped[int] = mapped_column(Integer, default=0)
    
    matches_home: Mapped[List["Match"]] = relationship('Match', foreign_keys='Match.home_team_id', back_populates='home_team_obj')
    matches_away: Mapped[List["Match"]] = relationship('Match', foreign_keys='Match.away_team_id', back_populates='away_team_obj')
    players: Mapped[List["Player"]] = relationship('Player', back_populates='team')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'logo_url': self.logo_url,
            'home_ground': self.home_ground,
            'wins': self.wins,
            'losses': self.losses,
            'matches_played': self.matches_played,
            'points': self.points
        }

class Player(db.Model):
    __tablename__ = 'players'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    team_id: Mapped[int] = mapped_column(Integer, ForeignKey('teams.id'), nullable=False)
    role: Mapped[Optional[str]] = mapped_column(String(50))
    jersey_number: Mapped[Optional[int]] = mapped_column(Integer)
    runs_scored: Mapped[int] = mapped_column(Integer, default=0)
    wickets_taken: Mapped[int] = mapped_column(Integer, default=0)
    matches_played: Mapped[int] = mapped_column(Integer, default=0)
    
    team: Mapped["Team"] = relationship('Team', back_populates='players')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'team_id': self.team_id,
            'role': self.role,
            'jersey_number': self.jersey_number,
            'runs_scored': self.runs_scored,
            'wickets_taken': self.wickets_taken,
            'matches_played': self.matches_played
        }

class Match(db.Model):
    __tablename__ = 'matches'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    match_number: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)
    home_team_id: Mapped[int] = mapped_column(Integer, ForeignKey('teams.id'), nullable=False)
    away_team_id: Mapped[int] = mapped_column(Integer, ForeignKey('teams.id'), nullable=False)
    venue: Mapped[Optional[str]] = mapped_column(String(150))
    scheduled_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default='Scheduled')
    home_team_score: Mapped[int] = mapped_column(Integer, default=0)
    away_team_score: Mapped[int] = mapped_column(Integer, default=0)
    home_team_wickets: Mapped[int] = mapped_column(Integer, default=0)
    away_team_wickets: Mapped[int] = mapped_column(Integer, default=0)
    overs_completed: Mapped[float] = mapped_column(Float, default=0)
    result: Mapped[Optional[str]] = mapped_column(String(200))
    toss_winner: Mapped[Optional[str]] = mapped_column(String(100))
    toss_decision: Mapped[Optional[str]] = mapped_column(String(50))
    man_of_match: Mapped[Optional[str]] = mapped_column(String(150))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    home_team_obj: Mapped["Team"] = relationship('Team', foreign_keys=[home_team_id], back_populates='matches_home')
    away_team_obj: Mapped["Team"] = relationship('Team', foreign_keys=[away_team_id], back_populates='matches_away')
    commentary_entries: Mapped[List["Commentary"]] = relationship('Commentary', back_populates='match', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'match_number': self.match_number,
            'home_team_id': self.home_team_id,
            'away_team_id': self.away_team_id,
            'home_team': self.home_team_obj.to_dict() if self.home_team_obj else None,
            'away_team': self.away_team_obj.to_dict() if self.away_team_obj else None,
            'venue': self.venue,
            'scheduled_date': self.scheduled_date.isoformat(),
            'status': self.status,
            'home_team_score': self.home_team_score,
            'away_team_score': self.away_team_score,
            'home_team_wickets': self.home_team_wickets,
            'away_team_wickets': self.away_team_wickets,
            'overs_completed': self.overs_completed,
            'result': self.result,
            'toss_winner': self.toss_winner,
            'toss_decision': self.toss_decision,
            'man_of_match': self.man_of_match,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Commentary(db.Model):
    __tablename__ = 'commentary'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    match_id: Mapped[int] = mapped_column(Integer, ForeignKey('matches.id'), nullable=False)
    ball_number: Mapped[float] = mapped_column(Float, nullable=False)
    batsman: Mapped[Optional[str]] = mapped_column(String(150))
    bowler: Mapped[Optional[str]] = mapped_column(String(150))
    description: Mapped[Optional[str]] = mapped_column(Text)
    runs: Mapped[int] = mapped_column(Integer, default=0)
    is_wicket: Mapped[bool] = mapped_column(Boolean, default=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    match: Mapped["Match"] = relationship('Match', back_populates='commentary_entries')
    
    def to_dict(self):
        return {
            'id': self.id,
            'match_id': self.match_id,
            'ball_number': self.ball_number,
            'batsman': self.batsman,
            'bowler': self.bowler,
            'description': self.description,
            'runs': self.runs,
            'is_wicket': self.is_wicket,
            'timestamp': self.timestamp.isoformat()
        }
