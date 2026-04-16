import React from 'react';
import { Trophy, Calendar, Users, BarChart2 } from 'lucide-react';
import './Navigation.css';

interface NavigationProps {
  currentPage: string;
  setCurrentPage: (page: string) => void;
}

const Navigation: React.FC<NavigationProps> = ({ currentPage, setCurrentPage }) => {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: BarChart2 },
    { id: 'standings', label: 'Standings', icon: Trophy },
    { id: 'matches', label: 'Matches', icon: Calendar },
    { id: 'players', label: 'Players', icon: Users },
  ];

  return (
    <nav className="navigation">
      <div className="nav-header">
        <h1>🏏 IPL 2026</h1>
      </div>
      <ul className="nav-links">
        {navItems.map(item => (
          <li key={item.id}>
            <button
              className={`nav-link ${currentPage === item.id ? 'active' : ''}`}
              onClick={() => setCurrentPage(item.id)}
            >
              <item.icon size={20} />
              <span>{item.label}</span>
            </button>
          </li>
        ))}
      </ul>
    </nav>
  );
};

export default Navigation;
