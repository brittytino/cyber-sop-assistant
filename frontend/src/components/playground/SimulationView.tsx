import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Send, ShieldAlert, Wifi, Battery, Signal, User } from 'lucide-react';

interface SimulationViewProps {
    scenario: {
        scenario_text: string;
        sender_name: string;
        context_notes: string;
        channel?: string; // Passed from parent if needed for UI tweaks
    };
    onEvaluate: (action: string) => void;
    loading: boolean;
}

const SimulationView: React.FC<SimulationViewProps> = ({ scenario, onEvaluate, loading }) => {
    const [actionText, setActionText] = useState('');

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (!actionText.trim()) return;
        onEvaluate(actionText);
    };

    return (
        <div style={{ height: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>

            {/* Phone Mockup */}
            <div className="phone-mockup" style={{
                width: '100%',
                maxWidth: '400px',
                background: 'var(--bg-primary)',
                border: '8px solid var(--border)',
                borderRadius: '32px',
                overflow: 'hidden',
                boxShadow: '0 20px 50px -10px rgba(0,0,0,0.5)',
                display: 'flex',
                flexDirection: 'column',
                height: '650px',
                position: 'relative'
            }}>
                {/* Status Bar */}
                <div style={{ padding: '12px 24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', background: 'var(--bg-input)', color: 'var(--text-secondary)', fontSize: '12px' }}>
                    <span>9:41</span>
                    <div style={{ display: 'flex', gap: '6px' }}>
                        <Signal size={12} />
                        <Wifi size={12} />
                        <Battery size={12} />
                    </div>
                </div>

                {/* App Header */}
                <div style={{ padding: '16px', background: 'var(--bg-card)', borderBottom: '1px solid var(--border)', display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <div style={{ width: '40px', height: '40px', borderRadius: '50%', background: 'var(--bg-hover)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--text-secondary)' }}>
                        <User size={20} />
                    </div>
                    <div>
                        <div style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{scenario.sender_name}</div>
                        <div style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>+91 98XXX XXXXX</div>
                    </div>
                </div>

                {/* Chat Body */}
                <div style={{ flex: 1, padding: '20px', background: 'var(--bg-primary)', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '20px' }}>

                    {/* Timestamp */}
                    <div style={{ textAlign: 'center', fontSize: '11px', color: 'var(--text-placeholder)', marginBottom: '10px' }}>
                        Today, 9:42 AM
                    </div>

                    {/* The Scam Message */}
                    <motion.div
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        className="chat-bubble"
                        style={{
                            background: 'var(--bg-card)',
                            padding: '16px',
                            borderRadius: '16px 16px 16px 2px',
                            color: 'var(--text-primary)',
                            boxShadow: 'var(--shadow-card)',
                            border: '1px solid var(--border)',
                            fontSize: '15px',
                            lineHeight: 1.5
                        }}
                    >
                        {scenario.scenario_text}
                    </motion.div>

                    {/* Context Note (Simulated Warning) */}
                    {scenario.context_notes && (
                        <div style={{ fontSize: '11px', color: '#eab308', textAlign: 'center', marginTop: '-10px', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '4px' }}>
                            <ShieldAlert size={12} /> {scenario.context_notes}
                        </div>
                    )}
                </div>

                {/* Action Area */}
                <div style={{ padding: '16px', background: 'var(--bg-card)', borderTop: '1px solid var(--border)' }}>
                    <p style={{ fontSize: '13px', color: 'var(--text-secondary)', marginBottom: '12px', fontWeight: 600 }}>
                        What would you do?
                    </p>

                    {/* Quick Actions */}
                    <div style={{ display: 'flex', gap: '8px', overflowX: 'auto', paddingBottom: '12px', marginBottom: '8px' }}>
                        {[
                            { label: 'Block Sender', color: '#ef4444' },
                            { label: 'Click Link', color: '#3b82f6' },
                            { label: 'Ignore', color: '#64748b' },
                            { label: 'Pay Money', color: '#eab308' },
                            { label: 'Verify Source', color: '#10b981' }
                        ].map(act => (
                            <button
                                key={act.label}
                                onClick={() => onEvaluate(act.label)}
                                disabled={loading}
                                style={{
                                    whiteSpace: 'nowrap',
                                    padding: '6px 12px',
                                    borderRadius: '20px',
                                    border: `1px solid ${act.color}`,
                                    color: act.color,
                                    background: 'transparent',
                                    fontSize: '12px',
                                    cursor: 'pointer',
                                    fontWeight: 500
                                }}
                            >
                                {act.label}
                            </button>
                        ))}
                    </div>

                    {/* Free Text Input */}
                    <form onSubmit={handleSubmit} style={{ display: 'flex', gap: '8px' }}>
                        <input
                            type="text"
                            value={actionText}
                            onChange={(e) => setActionText(e.target.value)}
                            placeholder="Type your own action..."
                            disabled={loading}
                            style={{
                                flex: 1,
                                padding: '10px 14px',
                                borderRadius: '20px',
                                border: '1px solid var(--border)',
                                background: 'var(--bg-input)',
                                color: 'var(--text-primary)',
                                fontSize: '14px',
                                outline: 'none'
                            }}
                        />
                        <button
                            type="submit"
                            disabled={loading || !actionText.trim()}
                            style={{
                                width: '40px', height: '40px', borderRadius: '50%',
                                background: 'var(--accent)', color: '#fff',
                                border: 'none', display: 'flex', alignItems: 'center', justifyContent: 'center',
                                cursor: 'pointer', opacity: loading ? 0.7 : 1
                            }}
                        >
                            <Send size={18} />
                        </button>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default SimulationView;
