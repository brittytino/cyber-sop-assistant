
import React, { useEffect, useState, useRef } from 'react';
import { chatAPI, Chat } from '../../api/client';
import {
  Plus, Library, Compass, Map,
  Menu, FileText, Trash2, Gamepad2, LogOut, Share2, MoreHorizontal
} from 'lucide-react';
import DeleteModal from '../common/DeleteModal';

interface SidebarProps {
  currentView: string;
  onViewChange: (view: 'chat' | 'resources' | 'police' | 'docs' | 'playground') => void;
  isMobileOpen?: boolean;
  setIsMobileOpen?: (open: boolean) => void;
  activeChatId?: number | null;
  onChatSelect?: (id: number | null) => void;
  onLogout?: () => void;
  username?: string | null;
  theme?: 'light' | 'dark';
  toggleTheme?: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({
  currentView,
  onViewChange,
  isMobileOpen = false,
  setIsMobileOpen = () => { },
  activeChatId,
  onChatSelect = () => { },
  onLogout = () => { },
  username,
  theme = 'dark',
  toggleTheme = () => { }
}) => {
  const [chats, setChats] = useState<Chat[]>([]);
  const [collapsed, setCollapsed] = useState(false);
  const [deleteId, setDeleteId] = useState<number | null>(null);
  const [sharedId, setSharedId] = useState<number | null>(null);
  const [openMenuId, setOpenMenuId] = useState<number | null>(null);
  const menuRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    loadChats();
  }, [activeChatId]); // Reload when ID changes (creation/deletion)

  // Close menu when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setOpenMenuId(null);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const loadChats = async () => {
    try {
      const data = await chatAPI.getChats();
      setChats(data);
    } catch (error) {
      console.error('Failed to load chats:', error);
    }
  };

  const handleNewChat = () => {
    onChatSelect(null);
    onViewChange('chat');
    closeMobile();
  };

  const hasShare = (id: number) => {
    // Mock share function
    setSharedId(id);
    setTimeout(() => setSharedId(null), 2000);
    navigator.clipboard.writeText(`https://cybersop.ai/chat/${id}`);
    setOpenMenuId(null);
  }

  const handleDeleteClick = (id: number) => {
    setDeleteId(id);
    setOpenMenuId(null);
  }

  const confirmDelete = async () => {
    if (!deleteId) return;
    try {
      await chatAPI.deleteChat(deleteId);
      if (activeChatId === deleteId) {
        onChatSelect(null);
      }
      loadChats();
    } catch (error) {
      console.error('Failed to delete chat:', error);
    } finally {
      setDeleteId(null);
    }
  };

  const closeMobile = () => {
    setIsMobileOpen(false);
  };

  // Logout Confirmation State
  const [showLogoutConfirm, setShowLogoutConfirm] = useState(false);

  const handleLogoutClick = () => {
    setShowLogoutConfirm(true);
  };

  const confirmLogout = () => {
    setShowLogoutConfirm(false);
    onLogout();
  };

  return (
    <>
      <DeleteModal
        isOpen={!!deleteId}
        onClose={() => setDeleteId(null)}
        onConfirm={confirmDelete}
        title="Delete Thread?"
        message="This conversation will be permanently deleted."
      />

      {/* Logout Confirmation Modal */}
      {showLogoutConfirm && (
        <div style={{
          position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
          background: 'rgba(0,0,0,0.7)', backdropFilter: 'blur(4px)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          zIndex: 9999
        }} onClick={() => setShowLogoutConfirm(false)}>
          <div onClick={(e) => e.stopPropagation()} style={{
            background: 'var(--bg-card)',
            border: '1px solid var(--border)',
            borderRadius: '16px',
            padding: '24px',
            width: '90%', maxWidth: '320px',
            boxShadow: '0 20px 40px -10px rgba(0,0,0,0.5)',
            textAlign: 'center',
            display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '16px'
          }}>
            <div style={{
              width: '48px', height: '48px', borderRadius: '50%',
              background: 'rgba(239, 68, 68, 0.1)', color: '#ea580c',
              display: 'flex', alignItems: 'center', justifyContent: 'center'
            }}>
              <LogOut size={24} />
            </div>

            <div>
              <h3 style={{ margin: '0 0 8px 0', fontSize: '18px', fontWeight: 600, color: 'var(--text-primary)' }}>Sign Out?</h3>
              <p style={{ margin: 0, color: 'var(--text-secondary)', fontSize: '14px', lineHeight: 1.5 }}>
                Are you sure you want to end your session? You will need to login again to access your chats.
              </p>
            </div>

            <div style={{ display: 'flex', gap: '12px', width: '100%', marginTop: '8px' }}>
              <button
                onClick={() => setShowLogoutConfirm(false)}
                style={{
                  flex: 1, padding: '12px', borderRadius: '12px',
                  background: 'var(--bg-hover)', color: 'var(--text-primary)',
                  border: 'none', fontWeight: 600, cursor: 'pointer'
                }}
              >
                Cancel
              </button>
              <button
                onClick={confirmLogout}
                style={{
                  flex: 1, padding: '12px', borderRadius: '12px',
                  background: '#ea580c', color: '#fff',
                  border: 'none', fontWeight: 600, cursor: 'pointer',
                  boxShadow: '0 4px 12px rgba(239, 68, 68, 0.3)'
                }}
              >
                Log Out
              </button>
            </div>
          </div>
        </div>
      )}

      <div
        className={`sidebar ${collapsed ? 'collapsed' : ''} ${isMobileOpen ? 'open' : ''}`}
      >
        <div className="sidebar-header" style={{ justifyContent: collapsed ? 'center' : 'space-between' }}>
          {!collapsed && (
            <div className="logo-container">
              <span className="logo-icon" style={{ color: 'var(--accent)' }}>✶</span>
              <span className="logo-label">Cyber SOP</span>
            </div>
          )}

          <div style={{ display: 'flex', gap: '4px' }}>
            {/* Theme Toggle */}
            <button
              className="toggle-btn"
              onClick={toggleTheme}
              style={{
                background: 'transparent',
                border: 'none',
                color: 'var(--text-secondary)',
                cursor: 'pointer',
                padding: '8px',
                borderRadius: '6px',
                display: window.innerWidth <= 768 ? 'none' : 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}
              title={theme === 'dark' ? "Switch to Light Mode" : "Switch to Dark Mode"}
            >
              {theme === 'dark' ? (
                /* Sun Icon */
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="5" /><line x1="12" y1="1" x2="12" y2="3" /><line x1="12" y1="21" x2="12" y2="23" /><line x1="4.22" y1="4.22" x2="5.64" y2="5.64" /><line x1="18.36" y1="18.36" x2="19.78" y2="19.78" /><line x1="1" y1="12" x2="3" y2="12" /><line x1="21" y1="12" x2="23" y2="12" /><line x1="4.22" y1="19.78" x2="5.64" y2="18.36" /><line x1="18.36" y1="5.64" x2="19.78" y2="4.22" /></svg>
              ) : (
                /* Moon Icon */
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" /></svg>
              )}
            </button>

            <button
              className="toggle-btn"
              onClick={() => setCollapsed(!collapsed)}
              style={{
                background: 'transparent',
                border: 'none',
                color: 'var(--text-secondary)',
                cursor: 'pointer',
                padding: '8px',
                borderRadius: '6px',
                display: window.innerWidth <= 768 ? 'none' : 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}
              title={collapsed ? "Expand Sidebar" : "Collapse Sidebar"}
            >
              <Menu size={20} />
            </button>
          </div>
        </div>

        <div className="sidebar-content">
          <button className="new-chat-btn" onClick={handleNewChat}>
            <Plus size={20} />
            <span>New Thread</span>
          </button>

          {/* Library Section */}
          <div className="nav-label">Library</div>
          <div className="library-list" style={{ flex: 1, minHeight: 0, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '2px' }}>
            {chats.map(chat => (
              <div
                key={chat.id}
                className={`nav-item ${activeChatId === chat.id && currentView === 'chat' ? 'active' : ''}`}
                onClick={() => { onChatSelect(chat.id); closeMobile(); }}
                style={{ justifyContent: 'space-between', paddingRight: '8px', position: 'relative' }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px', overflow: 'hidden', flex: 1 }}>
                  <Library size={18} style={{ flexShrink: 0 }} />
                  <span style={{ whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{chat.title}</span>
                </div>

                {/* More Options Button */}
                <button
                  className="more-btn"
                  onClick={(e) => { e.stopPropagation(); setOpenMenuId(openMenuId === chat.id ? null : chat.id); }}
                >
                  <MoreHorizontal size={16} />
                </button>

                {/* Dropdown Menu */}
                {openMenuId === chat.id && (
                  <div className="chat-menu" ref={menuRef} onClick={(e) => e.stopPropagation()}>
                    <button onClick={() => hasShare(chat.id)} style={{ color: sharedId === chat.id ? '#10b981' : 'var(--text-secondary)' }}>
                      <Share2 size={14} />
                      <span>{sharedId === chat.id ? 'Copied' : 'Share'}</span>
                    </button>
                    <button onClick={() => handleDeleteClick(chat.id)} className="danger">
                      <Trash2 size={14} />
                      <span>Delete</span>
                    </button>
                  </div>
                )}
              </div>
            ))}
            {chats.length === 0 && <div style={{ padding: '0 12px', fontSize: '13px', color: '#666' }}>No recent threads</div>}
          </div>

          {/* Discover Section */}
          <div className="nav-label">Discover</div>
          <div
            className={`nav-item ${currentView === 'resources' ? 'active' : ''}`}
            onClick={() => { onViewChange('resources'); closeMobile(); }}
          >
            <Compass size={18} />
            <span>Resources</span>
          </div>
          <div
            className={`nav-item ${currentView === 'playground' ? 'active' : ''}`}
            onClick={() => { onViewChange('playground'); closeMobile(); }}
          >
            <Gamepad2 size={18} />
            <span>Playground</span>
          </div>

          <div
            className={`nav-item ${currentView === 'police' ? 'active' : ''}`}
            onClick={() => { onViewChange('police'); closeMobile(); }}
          >
            <Map size={18} />
            <span>Nearby Police</span>
          </div>

          <a
            className="nav-item"
            href="https://t.me/cybercrimeinfobot"
            target="_blank"
            rel="noopener noreferrer"
            style={{ textDecoration: 'none', color: 'inherit' }}
          >
            <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
              <img src="https://upload.wikimedia.org/wikipedia/commons/8/82/Telegram_logo.svg" alt="TG" width={18} height={18} />
              <span>Cyber Helpline Bot</span>
            </div>
          </a>

          <div style={{ marginTop: 'auto' }}>
            <div
              className={`nav-item ${currentView === 'docs' ? 'active' : ''}`}
              onClick={() => { onViewChange('docs'); closeMobile(); }}
            >
              <FileText size={18} />
              <span>API Docs</span>
            </div>
          </div>
        </div>

        {/* User Profile Section - Click to Logout */}
        <div className="user-profile" onClick={handleLogoutClick} title="Click to Log Out">
          <div className="user-avatar">
            {username ? username[0].toUpperCase() : 'U'}
          </div>
          {!collapsed && (
            <div className="user-info">
              <div className="user-name">{username || 'User'}</div>
              <div className="user-plan">Pro Member</div>
            </div>
          )}
          {!collapsed && (
            <LogOut size={16} color="#666" style={{ marginLeft: 'auto' }} />
          )}
        </div>

      </div>

      {isMobileOpen && (
        <div className="sidebar-overlay" onClick={() => setIsMobileOpen(false)} />
      )}

      <style>{`
        /* More Button */
        .more-btn {
            background: transparent;
            border: none;
            color: var(--text-secondary);
            padding: 4px;
            cursor: pointer;
            border-radius: 4px;
            opacity: 0;
            transition: opacity 0.2s;
        }
        .nav-item:hover .more-btn, .nav-item.active .more-btn { opacity: 1; }
        .more-btn:hover { color: var(--text-primary); background: var(--bg-hover); }

        /* Chat Menu Dropdown */
        .chat-menu {
            position: absolute;
            right: 10px;
            top: 30px;
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 4px;
            z-index: 100;
            min-width: 120px;
            box-shadow: var(--shadow-card);
            animation: fadeIn 0.15s ease-out;
        }
        .chat-menu button {
            display: flex;
            align-items: center;
            gap: 10px;
            width: 100%;
            padding: 8px 12px;
            background: transparent;
            border: none;
            color: var(--text-secondary);
            font-size: 13px;
            cursor: pointer;
            text-align: left;
            border-radius: 4px;
        }
        .chat-menu button:hover { background: var(--bg-hover); color: var(--text-primary); }
        .chat-menu button.danger:hover { background: rgba(239, 68, 68, 0.2); color: #ef4444; }

        @keyframes fadeIn { from { opacity: 0; transform: translateY(-5px); } to { opacity: 1; transform: translateY(0); } }
        
        /* User Profile Styles */
        .user-profile {
            margin-top: 10px;
            padding: 16px 14px;
            border-top: 1px solid var(--border);
            display: flex;
            align-items: center;
            gap: 12px;
            background: var(--bg-sidebar);
            cursor: pointer;
            transition: background 0.2s;
        }
        .user-profile:hover { background: var(--bg-hover); }
        .user-avatar {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            background: linear-gradient(135deg, #f97316, #ea580c);
            color: #fff;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 16px;
            flex-shrink: 0;
            box-shadow: 0 2px 8px rgba(249, 115, 22, 0.3);
        }
        .user-info { flex: 1; overflow: hidden; }
        .user-name { font-size: 14px; font-weight: 600; color: var(--text-primary); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        .user-plan { font-size: 11px; color: var(--text-secondary); }
      `}</style>
    </>
  );
};

export default Sidebar;

