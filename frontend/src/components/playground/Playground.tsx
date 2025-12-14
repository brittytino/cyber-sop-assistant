import React, { useState, useEffect } from 'react';
import ScenarioControls from './ScenarioControls';
import SimulationView from './SimulationView';
import FeedbackCard from './FeedbackCard';
import { playgroundAPI } from '../../api/client';
import { Trophy, ShieldCheck, AlertTriangle } from 'lucide-react';

const Playground: React.FC = () => {
    // State
    const [scenario, setScenario] = useState<any | null>(null);
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<any | null>(null);
    const [stats, setStats] = useState({ attempted: 0, safe: 0, risky: 0 });

    // Load Stats on Mount
    useEffect(() => {
        const saved = localStorage.getItem('cyber_sop_stats');
        if (saved) setStats(JSON.parse(saved));
    }, []);

    const updateStats = (status: string) => {
        const newStats = { ...stats, attempted: stats.attempted + 1 };
        if (status.toLowerCase() === 'safe') newStats.safe += 1;
        else newStats.risky += 1;

        setStats(newStats);
        localStorage.setItem('cyber_sop_stats', JSON.stringify(newStats));
    };

    const generateScenario = async (type: string, difficulty: string, channel: string) => {
        setLoading(true);
        try {
            const data = await playgroundAPI.generateScenario(type, difficulty, channel, "English"); // Default to English for now, can be improved
            setScenario({ ...data, channel });
            setResult(null);
        } catch (error) {
            console.error("Failed to generate:", error);
        } finally {
            setLoading(false);
        }
    };

    const evaluateAction = async (action: string) => {
        if (!scenario) return;
        setLoading(true);
        try {
            const data = await playgroundAPI.evaluateAction(scenario.scenario_text, action, "English");
            setResult(data);
            updateStats(data.status);
        } catch (error) {
            console.error("Failed to evaluate:", error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="content-pane" style={{ display: 'flex', flexDirection: 'column', height: '100%', overflow: 'hidden' }}>
            {/* Header / Stats Bar */}
            <div style={{
                padding: '16px 24px',
                borderBottom: '1px solid var(--border)',
                background: 'var(--bg-card)',
                display: 'flex', justifyContent: 'space-between', alignItems: 'center'
            }}>
                <h2 style={{ fontSize: '20px', fontWeight: 700, color: 'var(--text-primary)' }}>Cyber Playground</h2>

                <div style={{ display: 'flex', gap: '16px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '13px', color: 'var(--text-secondary)' }}>
                        <Trophy size={14} color="var(--accent)" />
                        <span>Attempted: <b>{stats.attempted}</b></span>
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '13px', color: '#10b981' }}>
                        <ShieldCheck size={14} />
                        <span>Safe: <b>{stats.safe}</b></span>
                    </div>
                </div>
            </div>

            {/* Split View */}
            <div style={{ flex: 1, display: 'flex', overflow: 'hidden' }}>

                {/* Left: Controls (Hidden on mobile if scenario active?) - For now side by side */}
                <div style={{
                    width: '350px',
                    borderRight: '1px solid var(--border)',
                    background: 'var(--bg-sidebar)',
                    display: scenario ? 'none' : 'block' // Hide on mobile logic could go here, but focusing on desktop split first
                }} className="desktop-panel">
                    <ScenarioControls onGenerate={generateScenario} loading={loading} />
                </div>

                {/* Right: Simulator */}
                <div style={{ flex: 1, position: 'relative', background: 'var(--bg-primary)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>

                    {!scenario && !loading && (
                        <div style={{ textAlign: 'center', color: 'var(--text-secondary)', maxWidth: '400px' }}>
                            <div style={{ width: '80px', height: '80px', background: 'var(--bg-card)', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 20px auto' }}>
                                <ShieldCheck size={40} color="var(--accent)" />
                            </div>
                            <h3 style={{ fontSize: '20px', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '10px' }}>Ready to Practice?</h3>
                            <p>Select a scenario type on the left to start your training simulation.</p>
                        </div>
                    )}

                    {scenario && (
                        <SimulationView
                            scenario={scenario}
                            onEvaluate={evaluateAction}
                            loading={loading}
                        />
                    )}

                    {/* Result Overlay */}
                    {result && (
                        <FeedbackCard
                            result={result}
                            onRetry={() => { setResult(null); generateScenario("UPI Fraud", "Intermediate", "WhatsApp"); }} // Quick retry logic needs state ref or just close
                            onNext={() => { setResult(null); setScenario(null); }}
                            onReset={() => { setResult(null); setScenario(null); }}
                        />
                    )}
                </div>
            </div>

            <style>{`
                @media (min-width: 1024px) {
                    .desktop-panel { display: block !important; }
                }
            `}</style>
        </div>
    );
};

export default Playground;
