import React, { useState, useEffect } from 'react';
import Sidebar from './components/layout/Sidebar';
import ChatWindow from './components/chat/ChatWindow';
import ResourceList from './components/resources/ResourceList';
import NearbyPolice from './components/police/NearbyPolice';
import Playground from './components/playground/Playground';
import SecurityTicker from './components/layout/SecurityTicker';
import AuthPage from './components/auth/AuthPage';
import './index.css';

type View = 'chat' | 'resources' | 'police' | 'docs' | 'playground';

const App: React.FC = () => {
  const [currentView, setCurrentView] = useState<View>('chat');
  const [isMobileOpen, setIsMobileOpen] = useState(false);
  const [activeChatId, setActiveChatId] = useState<number | null>(null);
  const [user, setUser] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const [theme, setTheme] = useState<'light' | 'dark'>('dark');

  // Restore session & Theme
  useEffect(() => {
    const token = localStorage.getItem('cyber_sop_token');
    const username = localStorage.getItem('cyber_sop_username');
    if (token && username) {
      setUser(username);
      // Restore active chat if any
      const savedId = localStorage.getItem('cyber_sop_active_chat');
      if (savedId) setActiveChatId(parseInt(savedId));
    }

    // Restore Theme
    const savedTheme = localStorage.getItem('cyber_sop_theme') as 'light' | 'dark';
    if (savedTheme) {
      setTheme(savedTheme);
      if (savedTheme === 'light') document.body.classList.add('light');
    }

    setIsLoading(false);
  }, []);

  const toggleTheme = () => {
    const newTheme = theme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);
    localStorage.setItem('cyber_sop_theme', newTheme);

    if (newTheme === 'light') {
      document.body.classList.add('light');
    } else {
      document.body.classList.remove('light');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('cyber_sop_token');
    localStorage.removeItem('cyber_sop_username');
    localStorage.removeItem('cyber_sop_active_chat');
    setUser(null);
    setCurrentView('chat');
  };

  const handleChatChange = (id: number | null) => {
    setActiveChatId(id);
    if (id) {
      localStorage.setItem('cyber_sop_active_chat', id.toString());
      setCurrentView('chat');
    } else {
      localStorage.removeItem('cyber_sop_active_chat');
    }
  };

  useEffect(() => {
    if (currentView === 'docs') {
      window.open('http://localhost:8000/docs', '_blank');
    }
  }, [currentView]);

  if (isLoading) return null; // Or a loading spinner

  if (!user) {
    return <AuthPage onLogin={(u) => setUser(u)} />;
  }

  return (
    <div className="app-root">
      <div className="app-shell">
        <Sidebar
          currentView={currentView}
          onViewChange={setCurrentView}
          isMobileOpen={isMobileOpen}
          setIsMobileOpen={setIsMobileOpen}
          activeChatId={activeChatId}
          onChatSelect={handleChatChange}
          onLogout={handleLogout}
          username={user}
          theme={theme}
          toggleTheme={toggleTheme}
        />
        <main className="main-pane">
          {/* Security Alert Ticker */}
          <SecurityTicker />

          {currentView === 'chat' && (
            <ChatWindow
              setIsMobileOpen={setIsMobileOpen}
              activeChatId={activeChatId}
              setActiveChatId={handleChatChange}
            />
          )}
          {currentView === 'resources' && <ResourceList />}
          {currentView === 'police' && <NearbyPolice />}
          {currentView === 'playground' && <Playground />}
          {currentView === 'docs' && (
            <div className="docs-redirect" style={{ padding: '2rem', textAlign: 'center', color: 'var(--text-secondary)' }}>
              <h2 style={{ color: 'var(--text-primary)' }}>API Documentation</h2>
              <p>Opening API docs in new tab...</p>
              <a
                href="http://localhost:8000/docs"
                target="_blank"
                rel="noopener noreferrer"
                style={{ color: 'var(--accent)', textDecoration: 'underline', marginTop: '1rem', display: 'inline-block' }}
              >
                Click here if not redirected
              </a>
            </div>
          )}
        </main>
      </div>
    </div>
  );
};

export default App;
