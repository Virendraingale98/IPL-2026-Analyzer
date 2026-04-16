import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Players.css';

const API_URL = 'http://localhost:5000';

interface Player {
  id: number;
  name: string;
  team_id: number;
  role: string;
  jersey_number: number;
  runs_scored: number;
  wickets_taken: number;
  matches_played: number;
}

interface Team {
  id: number;
  name: string;
}

const Players: React.FC = () => {
  const [players, setPlayers] = useState<Player[]>([]);
  const [teams, setTeams] = useState<Team[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedTeam, setSelectedTeam] = useState<number | null>(null);
  const [selectedRole, setSelectedRole] = useState('all');

  useEffect(() => {
    fetchTeams();
    fetchPlayers();
  }, []);

  const fetchTeams = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/teams`);
      setTeams(response.data);
    } catch (error) {
      console.error('Error fetching teams:', error);
    }
  };

  const fetchPlayers = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/players`);
      setPlayers(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching players:', error);
      setLoading(false);
    }
  };

  const filteredPlayers = players.filter(player => {
    if (selectedTeam && player.team_id !== selectedTeam) return false;
    if (selectedRole !== 'all' && player.role !== selectedRole) return false;
    return true;
  });

  if (loading) return <div className="loading">Loading players...</div>;

  const roles = ['all', 'Batsman', 'Bowler', 'All-rounder'];

  return (
    <div className="players-container">
      <h2>IPL 2026 Players</h2>

      <div className="filters">
        <select value={selectedTeam || ''} onChange={(e) => setSelectedTeam(e.target.value ? Number(e.target.value) : null)}>
          <option value="">All Teams</option>
          {teams.map(team => (
            <option key={team.id} value={team.id}>
              {team.name}
            </option>
          ))}
        </select>

        <select value={selectedRole} onChange={(e) => setSelectedRole(e.target.value)}>
          {roles.map(role => (
            <option key={role} value={role}>
              {role === 'all' ? 'All Roles' : role}
            </option>
          ))}
        </select>
      </div>

      <div className="players-grid">
        {filteredPlayers.map(player => (
          <div key={player.id} className="player-card">
            <div className="player-header">
              <strong>{player.name}</strong>
              <span className="jersey">#{player.jersey_number}</span>
            </div>
            <div className="player-role">{player.role}</div>
            <div className="player-stats">
              <div className="stat">
                <span>Matches</span>
                <strong>{player.matches_played}</strong>
              </div>
              <div className="stat">
                <span>Runs</span>
                <strong>{player.runs_scored}</strong>
              </div>
              <div className="stat">
                <span>Wickets</span>
                <strong>{player.wickets_taken}</strong>
              </div>
            </div>
          </div>
        ))}
      </div>

      {filteredPlayers.length === 0 && (
        <div className="no-players">No players found</div>
      )}
    </div>
  );
};

export default Players;
