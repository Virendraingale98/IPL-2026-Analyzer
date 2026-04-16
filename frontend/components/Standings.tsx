import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Standings.css';

const API_URL = 'http://localhost:5000';

interface Team {
  id: number;
  name: string;
  points: number;
  wins: number;
  losses: number;
  matches_played: number;
}

const Standings: React.FC = () => {
  const [standings, setStandings] = useState<Team[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStandings();
  }, []);

  const fetchStandings = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/standings`);
      setStandings(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching standings:', error);
      setLoading(false);
    }
  };

  if (loading) return <div className="loading">Loading standings...</div>;

  return (
    <div className="standings-container">
      <h2>IPL 2026 Standings</h2>
      <table className="standings-table">
        <thead>
          <tr>
            <th>Rank</th>
            <th>Team</th>
            <th>Matches</th>
            <th>Wins</th>
            <th>Losses</th>
            <th>Points</th>
          </tr>
        </thead>
        <tbody>
          {standings.map((team, index) => (
            <tr key={team.id}>
              <td>{index + 1}</td>
              <td>{team.name}</td>
              <td>{team.matches_played}</td>
              <td>{team.wins}</td>
              <td>{team.losses}</td>
              <td className="points">{team.points}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Standings;
