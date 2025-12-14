import React from 'react';
import { motion } from 'framer-motion';
import { CheckCircle, AlertTriangle, XCircle, RefreshCw, ChevronRight, LayoutGrid } from 'lucide-react';

interface FeedbackCardProps {
    result: {
        status: string; // Safe, Risky, Dangerous
        explanation: string;
        tips: string[];
    };
    onRetry: () => void;
    onNext: () => void;
    onReset: () => void;
}

const FeedbackCard: React.FC<FeedbackCardProps> = ({ result, onRetry, onNext, onReset }) => {

    const getStatusStyle = (status: string) => {
        switch (status.toLowerCase()) {
            case 'safe':
                return { color: '#10b981', bg: 'rgba(16, 185, 129, 0.1)', icon: CheckCircle, label: 'Excellent Choice' };
            case 'risky':
                return { color: '#f59e0b', bg: 'rgba(245, 158, 11, 0.1)', icon: AlertTriangle, label: 'Risky Move' };
            case 'dangerous':
                return { color: '#ef4444', bg: 'rgba(239, 68, 68, 0.1)', icon: XCircle, label: 'Dangerous Mistake' };
            default:
                return { color: '#64748b', bg: 'rgba(100, 116, 139, 0.1)', icon: AlertTriangle, label: 'Analysis Complete' };
        }
    };

    const style = getStatusStyle(result.status);

    return (
        <div style={{
            position: 'absolute', top: 0, left: 0, right: 0, bottom: 0,
            background: 'rgba(0,0,0,0.8)',
            backdropFilter: 'blur(8px)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            zIndex: 50
        }}>
            <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                style={{
                    width: '90%', maxWidth: '400px',
                    background: 'var(--bg-card)',
                    border: '1px solid var(--border)',
                    borderRadius: '24px',
                    padding: '32px',
                    textAlign: 'center',
                    boxShadow: '0 20px 60px -10px rgba(0,0,0,0.5)',
                    position: 'relative',
                    overflow: 'hidden'
                }}
            >
                {/* Colored Header Glow */}
                <div style={{
                    position: 'absolute', top: 0, left: 0, right: 0, height: '6px',
                    background: style.color
                }} />

                <div style={{
                    width: '64px', height: '64px', borderRadius: '50%',
                    background: style.bg, color: style.color,
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    margin: '0 auto 20px auto'
                }}>
                    <style.icon size={32} />
                </div>

                <h2 style={{ fontSize: '24px', fontWeight: 800, color: 'var(--text-primary)', marginBottom: '8px' }}>
                    {style.label}
                </h2>

                <div style={{
                    display: 'inline-block',
                    padding: '4px 12px', borderRadius: '20px',
                    background: style.bg, color: style.color,
                    fontSize: '12px', fontWeight: 700, marginBottom: '24px',
                    textTransform: 'uppercase'
                }}>
                    VERDICT: {result.status}
                </div>

                <p style={{ fontSize: '16px', color: 'var(--text-secondary)', lineHeight: 1.6, marginBottom: '24px' }}>
                    {result.explanation}
                </p>

                <div style={{ textAlign: 'left', background: 'var(--bg-input)', padding: '16px', borderRadius: '12px', marginBottom: '32px' }}>
                    <div style={{ fontSize: '11px', fontWeight: 700, color: 'var(--text-secondary)', textTransform: 'uppercase', marginBottom: '8px' }}>
                        Safety Tips
                    </div>
                    <ul style={{ margin: 0, paddingLeft: '20px', color: 'var(--text-primary)', fontSize: '14px', lineHeight: 1.5 }}>
                        {result.tips.map((tip, i) => (
                            <li key={i} style={{ marginBottom: '4px' }}>{tip}</li>
                        ))}
                    </ul>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
                    <button onClick={onReset} style={{ padding: '12px', borderRadius: '12px', border: '1px solid var(--border)', background: 'transparent', color: 'var(--text-primary)', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px' }}>
                        <LayoutGrid size={16} /> Menu
                    </button>
                    <button onClick={onRetry} style={{ padding: '12px', borderRadius: '12px', border: '1px solid var(--border)', background: 'transparent', color: 'var(--text-primary)', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px' }}>
                        <RefreshCw size={16} /> Retry
                    </button>
                </div>
            </motion.div>
        </div>
    );
};

export default FeedbackCard;
