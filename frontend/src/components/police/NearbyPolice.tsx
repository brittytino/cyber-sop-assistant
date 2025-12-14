import React, { useState, useEffect } from 'react';
import { policeAPI, PoliceStation } from '../../api/client';
import { MapPin, Search, Phone, Navigation, User, Mail, Shield, AlertTriangle } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const NearbyPolice: React.FC = () => {
  const [stations, setStations] = useState<PoliceStation[]>([]);
  const [loading, setLoading] = useState(false);
  const [city, setCity] = useState('');
  const [hasSearched, setHasSearched] = useState(false);

  // Debounce search
  useEffect(() => {
    const timer = setTimeout(() => {
      if (city.trim().length >= 2) {
        searchStations(city);
      } else if (city.trim().length === 0) {
        setStations([]);
        setHasSearched(false);
      }
    }, 500);

    return () => clearTimeout(timer);
  }, [city]);

  const searchStations = async (searchTerm: string) => {
    setLoading(true);
    setHasSearched(true);
    try {
      const data = await policeAPI.searchStations(searchTerm);
      setStations(data);
    } catch (error) {
      console.error('Failed to search stations:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (city.trim()) {
      searchStations(city);
    }
  };

  const container = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  const item = {
    hidden: { opacity: 0, y: 20 },
    show: { opacity: 1, y: 0 }
  };

  return (
    <div className="content-pane" style={{ position: 'relative', overflow: 'hidden' }}>
      <div style={{ maxWidth: '800px', margin: '0 auto', paddingTop: hasSearched ? '20px' : '15vh', transition: 'padding 0.5s ease' }}>

        <motion.div
          layout
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          style={{ textAlign: hasSearched ? 'left' : 'center', marginBottom: '32px' }}
        >
          <h2 style={{ fontSize: hasSearched ? '28px' : '48px', fontWeight: 800, marginBottom: '16px', color: 'var(--text-primary)' }}>
            Find Cyber Cells
          </h2>
          <p style={{ fontSize: hasSearched ? '14px' : '18px', color: 'var(--text-secondary)', maxWidth: hasSearched ? '100%' : '500px', margin: hasSearched ? '0' : '0 auto' }}>
            Locate nearest official cyber crime police stations and cells across India.
          </p>
        </motion.div>

        <motion.div
          layout
          className="search-box-container"
          style={{ width: '100%', marginBottom: '40px' }}
        >
          <form onSubmit={handleSearch} style={{ position: 'relative', display: 'flex', gap: '12px' }}>
            <div style={{ position: 'relative', flex: 1 }}>
              <Search size={20} style={{ position: 'absolute', left: '16px', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-placeholder)' }} />
              <input
                type="text"
                value={city}
                onChange={(e) => setCity(e.target.value)}
                placeholder="Enter City like 'Coimbatore' or 'Chennai'..."
                style={{
                  width: '100%',
                  padding: '16px 16px 16px 48px',
                  borderRadius: '16px',
                  border: '1px solid var(--border)',
                  background: 'var(--bg-input)',
                  color: 'var(--text-primary)',
                  fontSize: '16px',
                  outline: 'none',
                  boxShadow: '0 4px 20px rgba(0,0,0,0.1)',
                  transition: '0.2s'
                }}
                onFocus={(e) => e.target.style.borderColor = 'var(--accent)'}
                onBlur={(e) => e.target.style.borderColor = 'var(--border)'}
              />
            </div>
            {/* Removed button as per request for cleaner UI, but kept form for Enter key support */}
          </form>
        </motion.div>

        <AnimatePresence>
          {hasSearched && (
            <motion.div
              layout
              variants={container}
              initial="hidden"
              animate="show"
              exit={{ opacity: 0 }}
              style={{ display: 'grid', gap: '16px', paddingBottom: '40px' }}
            >
              {stations.length > 0 ? (
                stations.map(st => (
                  <motion.div
                    key={st.id}
                    variants={item}
                    className="police-card-modern"
                    whileHover={{ scale: 1.01, backgroundColor: 'var(--bg-hover)' }}
                    style={{
                      background: 'var(--bg-card)',
                      border: '1px solid var(--border)',
                      borderRadius: '16px',
                      padding: '24px',
                      position: 'relative',
                      overflow: 'hidden',
                      boxShadow: 'var(--shadow-card)'
                    }}
                  >
                    {st.is_cyber_cell && (
                      <div style={{
                        position: 'absolute', top: 0, right: 0,
                        background: 'rgba(14, 165, 233, 0.1)',
                        color: '#0ea5e9',
                        padding: '4px 12px',
                        fontSize: '11px',
                        fontWeight: 700,
                        borderBottomLeftRadius: '12px',
                        display: 'flex', alignItems: 'center', gap: '4px'
                      }}>
                        <Shield size={12} /> OFFICIAL CYBER CELL
                      </div>
                    )}

                    <div style={{ display: 'flex', gap: '16px', alignItems: 'flex-start' }}>
                      <div style={{
                        background: 'var(--bg-hover)',
                        padding: '12px',
                        borderRadius: '12px',
                        color: 'var(--text-secondary)'
                      }}>
                        <MapPin size={24} />
                      </div>

                      <div style={{ flex: 1 }}>
                        <h3 style={{ fontSize: '18px', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '8px', paddingRight: '120px' }}>
                          {st.name}
                        </h3>
                        <p style={{ color: 'var(--text-secondary)', fontSize: '14px', marginBottom: '12px' }}>
                          {st.address}, {st.city}
                        </p>

                        {(st.officer || st.phone) && (
                          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '12px', marginTop: '12px' }}>
                            {st.officer && (
                              <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '13px', color: 'var(--text-secondary)', background: 'var(--bg-hover)', padding: '4px 8px', borderRadius: '6px' }}>
                                <User size={14} /> {st.officer} <span style={{ opacity: 0.5 }}>| {st.designation}</span>
                              </div>
                            )}
                            {st.phone && (
                              <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '13px', color: 'var(--text-secondary)', background: 'var(--bg-hover)', padding: '4px 8px', borderRadius: '6px' }}>
                                <Phone size={14} /> {st.phone}
                              </div>
                            )}
                            {st.email && (
                              <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '13px', color: 'var(--text-secondary)', background: 'var(--bg-hover)', padding: '4px 8px', borderRadius: '6px' }}>
                                <Mail size={14} /> {st.email}
                              </div>
                            )}
                          </div>
                        )}
                      </div>

                      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                        <button
                          onClick={() => window.open(`https://maps.google.com/?q=${encodeURIComponent(st.name + ' ' + st.address)}`)}
                          style={{
                            background: 'var(--bg-hover)',
                            border: '1px solid var(--border)',
                            color: 'var(--text-primary)',
                            width: '40px',
                            height: '40px',
                            borderRadius: '10px',
                            cursor: 'pointer',
                            display: 'flex', alignItems: 'center', justifyContent: 'center',
                            transition: '0.2s'
                          }}
                          title="Get Directions"
                          onMouseEnter={(e) => e.currentTarget.style.borderColor = 'var(--text-primary)'}
                          onMouseLeave={(e) => e.currentTarget.style.borderColor = 'var(--border)'}
                        >
                          <Navigation size={18} />
                        </button>
                      </div>
                    </div>
                  </motion.div>
                ))
              ) : (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  style={{ textAlign: 'center', padding: '40px', color: 'var(--text-secondary)' }}
                >
                  <AlertTriangle size={48} style={{ marginBottom: '16px', opacity: 0.5 }} />
                  <p>No stations found in this area.</p>
                  <p style={{ fontSize: '13px', marginTop: '8px' }}>Try searching for a larger city or state name.</p>
                </motion.div>
              )}
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};

export default NearbyPolice;
