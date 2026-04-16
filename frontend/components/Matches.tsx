import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Socket } from 'socket.io-client';
import './Matches.css';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

interface Team {
  id: number;
  name: string;
  logo_url?: string;
}

interface Match {
  id: number;
  match_number: number;
  home_team: Team;
  away_team: Team;
  status: string;
  home_team_score: number;
  away_team_score: number;
  home_team_wickets: number;
  away_team_wickets: number;
  overs_completed: number;
  venue: string;
  scheduled_date: string;
  result?: string;
  man_of_match?: string;
}

interface MatchesProps {
  socket: Socket | null;
}

const Matches: React.FC<MatchesProps> = ({ socket }) => {
  const [matches, setMatches] = useState<Match[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    fetchMatches();

    if (socket) {
      socket.on('match_update', (updatedMatch: Match) => {
        setMatches(prev =>
          prev.map(m => m.id === updatedMatch.id ? updatedMatch : m)
        );
      });

      socket.on('match_created', (newMatch: Match) => {
        setMatches(prev => [...prev, newMatch]);
      });
    }

    return () => {
      if (socket) {
        socket.off('match_update');
        socket.off('match_created');
      }
    };
  }, [socket]);

  const fetchMatches = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/matches`);
      setMatches(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching matches:', error);
      setLoading(false);
    }
  };

  const filteredMatches = matches.filter(match => {
    if (filter === 'all') return true;
    return match.status.toLowerCase() === filter.toLowerCase();
  });

  if (loading) return <div className="loading">Loading matches...</div>;

  return (
    <div className="matches-container">
      <h2>IPL 2026 Matches</h2>
      
      <div className="filter-buttons">
        <button
          className={filter === 'all' ? 'active' : ''}
          onClick={() => setFilter('all')}
        >
          All
        </button>
        <button
          className={filter === 'scheduled' ? 'active' : ''}
          onClick={() => setFilter('scheduled')}
        >
          Upcoming
        </button>
        <button
          className={filter === 'live' ? 'active' : ''}
          onClick={() => setFilter('live')}
        >
          Live
        </button>
        <button
          className={filter === 'completed' ? 'active' : ''}
          onClick={() => setFilter('completed')}
        >
          Completed
        </button>
      </div>

      <div className="matches-list">
        {filteredMatches.map(match => (
          <div key={match.id} className={`match-card ${match.status.toLowerCase()}`}>
            <div className="match-header">
              <span className="match-number">Match #{match.match_number}</span>
              <span className={`status-badge ${match.status.toLowerCase()}`}>
                {match.status}
              </span>
            </div>

            <div className="match-body">
              <div className="team home-team">
                <h3>{match.home_team.name}</h3>
                {match.status === 'Completed' || match.status === 'Live' ? (
                  <div className="score">
                    <span className="runs">{match.home_team_score}</span>
                    <span className="wickets">/{match.home_team_wickets}</span>
                  </div>
                ) : (
                  <div className="vs">vs</div>
                )}
              </div>

              <div className="overs-info">
                {match.status === 'Live' && (
                  <span>{match.overs_completed} overs</span>
                )}
              </div>

              <div className="team away-team">
                {match.status === 'Completed' || match.status === 'Live' ? (
                  <div className="score">
                    <span className="runs">{match.away_team_score}</span>
                    <span className="wickets">/{match.away_team_wickets}</span>
                  </div>
                ) : (
                  <div className="vs">vs</div>
                )}
                <h3>{match.away_team.name}</h3>
              </div>
            </div>

            <div className="match-footer">
              <small>{match.venue}</small>
              <small>
                {new Date(match.scheduled_date).toLocaleDateString()} 
                {' '}
                {new Date(match.scheduled_date).toLocaleTimeString()}
              </small>
            </div>

            {match.result && (
              <div className="match-result">
                <p><strong>Result:</strong> {match.result}</p>
                {match.man_of_match && (
                  <p><strong>Man of Match:</strong> {match.man_of_match}</p>
                )}
              </div>
            )}
          </div>
        ))}
      </div>

      {filteredMatches.length === 0 && (
        <div className="no-matches">No matches found</div>
      )}
    </div>
  );
};

export default Matches;
