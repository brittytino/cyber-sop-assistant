import React from 'react';

const ALERTS = [
  "🔔 Security Alerts – CERT-In",
  "📅 Dec 12: CIVN-2025-0359: Multiple vulnerabilities in Drupal products",
  "CIVN-2025-0358: Multiple vulnerabilities in Zoom",
  "CIVN-2025-0357: Privilege escalation in Windows Cloud Files Mini Filter Driver",
  "CIAD-2025-0051: Multiple vulnerabilities in SAP products",
  "📅 Dec 11: CIAD-2025-0050: Multiple vulnerabilities in Fortinet products",
  "📅 Dec 10: CIAD-2025-0049: Multiple vulnerabilities in Microsoft products"
];

const SecurityTicker: React.FC = () => {
  return (
    <div className="ticker-container">
      <div className="ticker-track">
        {/* Duplicate content to ensure seamless infinite scroll */}
        {[...ALERTS, ...ALERTS, ...ALERTS].map((alert, i) => (
          <span key={i} className="ticker-item">
            {alert.includes('🔔') || alert.includes('📅') ? (
              <span style={{ color: '#f97316', fontWeight: 600 }}>{alert}</span>
            ) : (
              <span>{alert}</span>
            )}
            <span className="ticker-separator">•</span>
          </span>
        ))}
      </div>

      <style>{`
        .ticker-container {
          width: 100%;
          background: var(--bg-sidebar);
          border-bottom: 1px solid var(--border);
          overflow: hidden;
          white-space: nowrap;
          position: relative;
          z-index: 10;
          height: 36px;
          display: flex;
          align-items: center;
          flex-shrink: 0;
        }

        .ticker-track {
          display: inline-flex;
          align-items: center;
          animation: scroll-left 60s linear infinite;
          padding-left: 100%; /* Start from off-screen */
        }

        .ticker-item {
          display: inline-flex;
          align-items: center;
          font-size: 12px;
          color: var(--text-secondary);
          padding: 0 4px;
        }

        .ticker-separator {
          margin: 0 16px;
          color: var(--text-placeholder);
          font-size: 10px;
        }

        @keyframes scroll-left {
          0% { transform: translateX(0); }
          100% { transform: translateX(-100%); }
        }

        /* Hover to pause */
        .ticker-container:hover .ticker-track {
          animation-play-state: paused;
        }
      `}</style>
    </div>
  );
};

export default SecurityTicker;
