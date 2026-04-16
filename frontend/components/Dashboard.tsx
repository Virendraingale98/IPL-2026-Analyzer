import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Socket } from 'socket.io-client';
import './Dashboard.css';

const API_URL = 'http://localhost:5000';

interface Match {
  id: number;
  match_number: number;
  status: string;
  home_team: { name: string };
  away_team: { name: string };
  home_team_score: number;
  away_team_score: number;
}

interface DashboardProps {
  socket: Socket | null;
}

const Dashboard: React.FC<DashboardProps> = ({ socket }) => {
  const [liveMatches, setLiveMatches] = useState<Match[]>([]);
  const [upcomingMatches, setUpcomingMatches] = useState<Match[]>([]);
  const [totalMatches, setTotalMatches] = useState(0);

  useEffect(() => {
    fetchDashboardData();

    if (socket) {
      socket.on('match_update', (updatedMatch: Match) => {
        setLiveMatches(prev =>
          prev.map(m => m.id === updatedMatch.id ? updatedMatch : m)
        );
      });
    }
  }, [socket]);

  const fetchDashboardData = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/matches`);
      const allMatches = response.data;
      setTotalMatches(allMatches.length);
      setLiveMatches(allMatches.filter((m: Match) => m.status === 'Live'));
      setUpcomingMatches(allMatches.filter((m: Match) => m.status === 'Scheduled').slice(0, 5));
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    }
  };

  return (
    <div className="dashboard-container">
      <h1>IPL 2026 Dashboard</h1>
      
      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Matches</h3>
          <p className="stat-value">{totalMatches}</p>
        </div>
        <div className="stat-card live">
          <h3>🔴 Live Matches</h3>
          <p className="stat-value">{liveMatches.length}</p>
        </div>
        <div className="stat-card upcoming">
          <h3>📅 Upcoming</h3>
          <p className="stat-value">{upcomingMatches.length}</p>
        </div>
      </div>

      <div className="dashboard-section">
        <h2>Live Matches Now</h2>
        {liveMatches.length > 0 ? (
          <div className="live-matches">
            {liveMatches.map(match => (
              <div key={match.id} className="live-match-card">
                <span className="live-badge">🔴 LIVE</span>
                <div className="match-detail">
                  <strong>{match.home_team.name}</strong> {match.home_team_score}
                </div>
                <div className="vs-badge">VS</div>
                <div className="match-detail">
                  {match.away_team_score} <strong>{match.away_team.name}</strong>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="no-data">No live matches at the moment</p>
        )}
      </div>

      <div className="dashboard-section">
        <h2>Upcoming Matches</h2>
        {upcomingMatches.length > 0 ? (
          <ul className="upcoming-list">
            {upcomingMatches.map(match => (
              <li key={match.id}>
                Match #{match.match_number}: {match.home_team.name} vs {match.away_team.name}
              </li>
            ))}
          </ul>
        ) : (
          <p className="no-data">No upcoming matches</p>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
