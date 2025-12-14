import React, { useEffect, useState } from 'react';
import { resourcesAPI, Resource } from '../../api/client';
import { ExternalLink, Shield, Phone, Globe, BookOpen, AlertTriangle } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const ResourceList: React.FC = () => {
  const [resources, setResources] = useState<Resource[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadResources();
  }, []);

  const loadResources = async () => {
    try {
      const data = await resourcesAPI.getResources();
      setResources(data);
    } catch (error) {
      console.error('Failed to load resources:', error);
    } finally {
      setLoading(false);
    }
  };

  const getCategoryStyle = (category: string) => {
    if (category.includes('Helpline') || category.includes('Emergency'))
      return { icon: <Phone size={20} />, color: '#ef4444', label: 'Emergency', bg: 'rgba(239, 68, 68, 0.1)' };
    if (category.includes('Security') || category.includes('Tools') || category.includes('Advisory'))
      return { icon: <Shield size={20} />, color: '#0ea5e9', label: 'Security', bg: 'rgba(14, 165, 233, 0.1)' };
    if (category.includes('Report') || category.includes('Portal'))
      return { icon: <AlertTriangle size={20} />, color: '#f59e0b', label: 'Reporting', bg: 'rgba(245, 158, 11, 0.1)' };
    return { icon: <Globe size={20} />, color: '#8b5cf6', label: 'Resource', bg: 'rgba(139, 92, 246, 0.1)' };
  };

  const container = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: { staggerChildren: 0.05 }
    }
  };

  const item = {
    hidden: { opacity: 0, scale: 0.9, y: 20 },
    show: { opacity: 1, scale: 1, y: 0 }
  };

  return (
    <div className="content-pane" style={{ padding: '0', height: '100%', overflowY: 'auto' }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '40px 20px' }}>
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          style={{ marginBottom: '40px' }}
        >
          <h2 style={{ fontSize: '36px', fontWeight: 800, color: 'var(--text-primary)', letterSpacing: '-0.5px', marginBottom: '10px' }}>
            Cyber Security <span style={{ color: 'var(--accent)' }}>Resources</span>
          </h2>
          <p style={{ color: 'var(--text-secondary)', fontSize: '18px', maxWidth: '600px', lineHeight: 1.6 }}>
            Access official government portals, emergency helplines, and essential security tools to stay safe online.
          </p>
        </motion.div>

        {loading ? (
          <div style={{ display: 'flex', justifyContent: 'center', padding: '100px' }}>
            <div className="loading-dots"></div>
          </div>
        ) : (
          <motion.div
            className="resource-grid"
            variants={container}
            initial="hidden"
            animate="show"
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))',
              gap: '24px'
            }}
          >
            {resources.map(res => {
              const style = getCategoryStyle(res.category);
              return (
                <motion.a
                  key={res.id}
                  href={res.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  variants={item}
                  whileHover={{ y: -8, boxShadow: 'var(--shadow-card)' }}
                  style={{
                    textDecoration: 'none',
                    display: 'flex',
                    flexDirection: 'column',
                    background: 'var(--bg-card)',
                    border: '1px solid var(--border)',
                    borderRadius: '24px',
                    padding: '28px',
                    position: 'relative',
                    overflow: 'hidden',
                    transition: 'border 0.2s, background 0.2s',
                    cursor: 'pointer',
                    boxShadow: 'var(--shadow-card)'
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.borderColor = style.color;
                    e.currentTarget.style.background = 'var(--bg-hover)';
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.borderColor = 'var(--border)';
                    e.currentTarget.style.background = 'var(--bg-card)';
                  }}
                >
                  <div style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'flex-start',
                    marginBottom: '20px'
                  }}>
                    <div style={{
                      background: style.bg,
                      color: style.color,
                      padding: '12px',
                      borderRadius: '16px',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      boxShadow: `0 0 20px ${style.bg}`
                    }}>
                      {style.icon}
                    </div>
                    <div style={{
                      background: 'var(--bg-hover)',
                      borderRadius: '12px',
                      padding: '8px',
                      color: 'var(--text-secondary)',
                      transition: '0.2s'
                    }} className="icon-hover">
                      <ExternalLink size={18} />
                    </div>
                  </div>

                  <h3 style={{
                    color: 'var(--text-primary)',
                    fontSize: '20px',
                    fontWeight: 700,
                    marginBottom: '12px',
                    lineHeight: 1.3
                  }}>
                    {res.name}
                  </h3>

                  <p style={{
                    color: 'var(--text-secondary)',
                    fontSize: '15px',
                    lineHeight: 1.6,
                    flex: 1,
                    marginBottom: '10px'
                  }}>
                    {res.description}
                  </p>
                  <div style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    fontSize: '12px',
                    fontWeight: 600,
                    color: style.color,
                    letterSpacing: '0.5px',
                    marginTop: 'auto'
                  }}>
                    {style.label.toUpperCase()}
                  </div>
                </motion.a>
              );
            })}
          </motion.div>
        )}
      </div>
    </div>
  );
};

export default ResourceList;
