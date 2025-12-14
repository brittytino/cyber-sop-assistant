import React from 'react';
import { motion } from 'framer-motion';
import { Shield, Smartphone, Mail, MessageSquare, PhoneCall, AlertTriangle, CreditCard, Gift, Heart, Briefcase } from 'lucide-react';

interface ScenarioControlsProps {
    onGenerate: (type: string, difficulty: string, channel: string) => void;
    loading: boolean;
}

const SCENARIO_TYPES = [
    { id: 'UPI Fraud', label: 'UPI / Payment', icon: CreditCard, color: '#f97316' },
    { id: 'Phishing', label: 'Phishing Link', icon: AlertTriangle, color: '#ef4444' },
    { id: 'Job Scam', label: 'Job offer', icon: Briefcase, color: '#3b82f6' },
    { id: 'Lottery', label: 'Lottery / Prize', icon: Gift, color: '#eab308' },
    { id: 'Sextortion', label: 'Sextortion', icon: Heart, color: '#ec4899' },
    { id: 'Customer Care', label: 'Fake Care', icon: PhoneCall, color: '#8b5cf6' },
];

const CHANNELS = [
    { id: 'WhatsApp', icon: MessageSquare },
    { id: 'SMS', icon: Smartphone },
    { id: 'Email', icon: Mail },
];

const ScenarioControls: React.FC<ScenarioControlsProps> = ({ onGenerate, loading }) => {
    const [selectedType, setSelectedType] = React.useState(SCENARIO_TYPES[0].id);
    const [difficulty, setDifficulty] = React.useState('Intermediate');
    const [selectedChannel, setSelectedChannel] = React.useState('WhatsApp');

    return (
        <div className="glass-panel" style={{ padding: '24px', height: '100%', overflowY: 'auto' }}>
            <h2 style={{ fontSize: '24px', fontWeight: 700, marginBottom: '24px', color: 'var(--text-primary)' }}>
                Setup Scenario
            </h2>

            {/* Scenario Type Grid */}
            <div style={{ marginBottom: '32px' }}>
                <label style={{ display: 'block', fontSize: '13px', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '12px', textTransform: 'uppercase' }}>
                    Type of Threat
                </label>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '12px' }}>
                    {SCENARIO_TYPES.map(type => (
                        <motion.button
                            key={type.id}
                            whileTap={{ scale: 0.98 }}
                            onClick={() => setSelectedType(type.id)}
                            style={{
                                display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '8px',
                                padding: '16px',
                                background: selectedType === type.id ? 'var(--bg-hover)' : 'var(--bg-input)',
                                border: `1px solid ${selectedType === type.id ? type.color : 'var(--border)'}`,
                                borderRadius: '12px',
                                color: selectedType === type.id ? 'var(--text-primary)' : 'var(--text-secondary)',
                                cursor: 'pointer',
                                transition: 'all 0.2s',
                                textAlign: 'center'
                            }}
                        >
                            <type.icon size={24} color={selectedType === type.id ? type.color : 'currentColor'} />
                            <span style={{ fontSize: '13px', fontWeight: 500 }}>{type.label}</span>
                        </motion.button>
                    ))}
                </div>
            </div>

            {/* Difficulty Slider */}
            <div style={{ marginBottom: '32px' }}>
                <label style={{ display: 'block', fontSize: '13px', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '12px', textTransform: 'uppercase' }}>
                    Difficulty Level
                </label>
                <div style={{ display: 'flex', gap: '4px', background: 'var(--bg-input)', padding: '4px', borderRadius: '12px', border: '1px solid var(--border)' }}>
                    {['Beginner', 'Intermediate', 'Advanced'].map(diff => (
                        <button
                            key={diff}
                            onClick={() => setDifficulty(diff)}
                            style={{
                                flex: 1,
                                padding: '8px',
                                background: difficulty === diff ? 'var(--bg-card)' : 'transparent',
                                color: difficulty === diff ? 'var(--text-primary)' : 'var(--text-secondary)',
                                borderRadius: '8px',
                                border: 'none',
                                fontSize: '13px',
                                fontWeight: 500,
                                cursor: 'pointer',
                                boxShadow: difficulty === diff ? 'var(--shadow-card)' : 'none',
                                transition: '0.2s'
                            }}
                        >
                            {diff}
                        </button>
                    ))}
                </div>
            </div>

            {/* Channel Selection */}
            <div style={{ marginBottom: '32px' }}>
                <label style={{ display: 'block', fontSize: '13px', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '12px', textTransform: 'uppercase' }}>
                    Channel
                </label>
                <div style={{ display: 'flex', gap: '12px' }}>
                    {CHANNELS.map(ch => (
                        <button
                            key={ch.id}
                            onClick={() => setSelectedChannel(ch.id)}
                            style={{
                                flex: 1,
                                display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px',
                                padding: '12px',
                                background: selectedChannel === ch.id ? 'var(--bg-hover)' : 'var(--bg-input)',
                                border: `1px solid ${selectedChannel === ch.id ? 'var(--accent)' : 'var(--border)'}`,
                                borderRadius: '12px',
                                color: selectedChannel === ch.id ? 'var(--text-primary)' : 'var(--text-secondary)',
                                cursor: 'pointer',
                                transition: '0.2s'
                            }}
                        >
                            <ch.icon size={18} />
                            <span style={{ fontSize: '13px', fontWeight: 500 }}>{ch.id}</span>
                        </button>
                    ))}
                </div>
            </div>

            {/* Start Button */}
            <button
                onClick={() => onGenerate(selectedType, difficulty, selectedChannel)}
                disabled={loading}
                style={{
                    width: '100%',
                    padding: '16px',
                    background: 'var(--accent)',
                    color: '#fff',
                    border: 'none',
                    borderRadius: '16px',
                    fontSize: '16px',
                    fontWeight: 700,
                    cursor: loading ? 'wait' : 'pointer',
                    opacity: loading ? 0.7 : 1,
                    display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '10px',
                    boxShadow: '0 4px 12px rgba(249, 115, 22, 0.3)'
                }}
            >
                {loading ? 'Generating Simulation...' : 'Start Simulation'}
                {!loading && <Shield size={18} />}
            </button>
        </div>
    );
};

export default ScenarioControls;
