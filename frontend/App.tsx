import React, { useState, useEffect } from 'react';
import axios from 'axios';
import io from 'socket.io-client';
import Dashboard from './components/Dashboard';
import Standings from './components/Standings';
import Matches from './components/Matches';
import Players from './components/Players';
import Navigation from './components/Navigation';
import './App.css';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

function App() {
  const [currentPage, setCurrentPage] = useState('dashboard');
  const [socket, setSocket] = useState(null);
  const [liveMatches, setLiveMatches] = useState([]);

  useEffect(() => {
    // Initialize WebSocket connection
    const newSocket = io(API_URL);
    setSocket(newSocket);

    newSocket.on('connect', () => {
      console.log('Connected to live server');
    });

    newSocket.on('match_update', (data) => {
      console.log('Match update received:', data);
      setLiveMatches(prev => 
        prev.map(m => m.id === data.id ? data : m)
      );
    });

    newSocket.on('new_commentary', (data) => {
      console.log('New commentary:', data);
    });

    return () => {
      newSocket.disconnect();
    };
  }, []);

  const renderPage = () => {
    switch(currentPage) {
      case 'dashboard':
        return <Dashboard socket={socket} />;
      case 'standings':
        return <Standings />;
      case 'matches':
        return <Matches socket={socket} />;
      case 'players':
        return <Players />;
      default:
        return <Dashboard socket={socket} />;
    }
  };

  return (
    <div className="App">
      <Navigation currentPage={currentPage} setCurrentPage={setCurrentPage} />
      <main className="main-content">
        {renderPage()}
      </main>
    </div>
  );
}

export default App;
