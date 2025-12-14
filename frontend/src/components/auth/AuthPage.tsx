import React, { useState } from 'react';
import { authAPI } from '../../api/client';
import { Shield, Lock, User, ArrowRight, Loader2, AlertCircle } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface AuthPageProps {
    onLogin: (username: string) => void;
}

const AuthPage: React.FC<AuthPageProps> = ({ onLogin }) => {
    const [isLogin, setIsLogin] = useState(true);
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!username || !password) {
            setError("Please fill in all fields");
            return;
        }

        if (!isLogin && password !== confirmPassword) {
            setError("Passwords do not match");
            return;
        }

        setLoading(true);
        setError(null);

        try {
            if (isLogin) {
                // Login
                const data = await authAPI.login(username, password);
                localStorage.setItem('cyber_sop_token', data.access_token);
                localStorage.setItem('cyber_sop_username', data.username);
                onLogin(data.username);
            } else {
                // Signup
                const data = await authAPI.signup(username, password);
                localStorage.setItem('cyber_sop_token', data.access_token);
                localStorage.setItem('cyber_sop_username', data.username);
                onLogin(data.username);
            }
        } catch (err: any) {
            console.error(err);
            if (err.response?.status === 401) {
                setError("Invalid credentials");
            } else if (err.response?.status === 400 && !isLogin) {
                setError("Username already exists");
            } else {
                setError("Authentication failed. Please try again.");
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="auth-container">
            {/* Visual Side */}
            <div className="auth-brand">
                <div className="brand-content">
                    <motion.div
                        initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.8 }}
                        style={{ fontSize: '4rem', color: '#f97316', marginBottom: '1rem' }}
                    >
                        ✶
                    </motion.div>
                    <motion.h1
                        initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2, duration: 0.8 }}
                        style={{ fontSize: '2.5rem', fontWeight: 700, marginBottom: '0.5rem' }}
                    >
                        Cyber SOP Assistant
                    </motion.h1>
                    <motion.p
                        initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4, duration: 0.8 }}
                        style={{ fontSize: '1.2rem', color: 'var(--text-secondary)', maxWidth: '400px', lineHeight: 1.6 }}
                    >
                        Your AI-powered companion for cybersecurity reporting, safety checklists, and awareness training.
                    </motion.p>
                </div>
            </div>

            {/* Form Side */}
            <div className="auth-form-wrapper">
                <div className="auth-box">
                    <h2 style={{ fontSize: '1.8rem', fontWeight: 700, marginBottom: '2rem', display: 'flex', alignItems: 'center', gap: '12px' }}>
                        {isLogin ? <Lock size={28} color="#f97316" /> : <Shield size={28} color="#f97316" />}
                        {isLogin ? 'Welcome Back' : 'Create Account'}
                    </h2>

                    <form onSubmit={handleSubmit}>
                        <div className="input-group">
                            <label>Username</label>
                            <div className="input-wrapper">
                                <User size={18} />
                                <input
                                    type="text"
                                    placeholder="Enter username"
                                    value={username}
                                    onChange={(e) => setUsername(e.target.value)}
                                />
                            </div>
                        </div>

                        <div className="input-group">
                            <label>Password</label>
                            <div className="input-wrapper">
                                <Lock size={18} />
                                <input
                                    type="password"
                                    placeholder="Enter password"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                />
                            </div>
                        </div>

                        <AnimatePresence>
                            {!isLogin && (
                                <motion.div
                                    initial={{ height: 0, opacity: 0 }}
                                    animate={{ height: 'auto', opacity: 1 }}
                                    exit={{ height: 0, opacity: 0 }}
                                    className="input-group"
                                >
                                    <label>Confirm Password</label>
                                    <div className="input-wrapper">
                                        <Lock size={18} />
                                        <input
                                            type="password"
                                            placeholder="Confirm password"
                                            value={confirmPassword}
                                            onChange={(e) => setConfirmPassword(e.target.value)}
                                        />
                                    </div>
                                </motion.div>
                            )}
                        </AnimatePresence>

                        {error && (
                            <div className="error-msg">
                                <AlertCircle size={16} />
                                <span>{error}</span>
                            </div>
                        )}

                        <button type="submit" className="submit-btn" disabled={loading}>
                            {loading ? <Loader2 className="spin" /> : (isLogin ? 'Log In' : 'Sign Up')}
                            {!loading && <ArrowRight size={18} />}
                        </button>
                    </form>

                    <div className="switch-text">
                        {isLogin ? "Don't have an account?" : "Already have an account?"}
                        <span onClick={() => { setIsLogin(!isLogin); setError(null); }}>
                            {isLogin ? " Create Account" : " Login"}
                        </span>
                    </div>
                </div>
            </div>

            <style>{`
        .auth-container { display: flex; height: 100vh; width: 100vw; overflow: hidden; background: var(--bg-primary); color: var(--text-primary); }
        .auth-brand { flex: 1; background: var(--bg-sidebar); display: flex; items: center; justify-content: center; position: relative; border-right: 1px solid var(--border); }
        .brand-content { padding: 4rem; z-index: 10; display: flex; flex-direction: column; justify-content: center; height: 100%; }
        
        .auth-form-wrapper { flex: 1; display: flex; align-items: center; justify-content: center; background: var(--bg-primary); }
        .auth-box { width: 100%; max-width: 420px; padding: 40px; }
        
        .input-group { margin-bottom: 20px; }
        .input-group label { display: block; font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 8px; font-weight: 500; }
        .input-wrapper { display: flex; align-items: center; background: var(--bg-input); border: 1px solid var(--border); border-radius: 12px; padding: 0 16px; transition: border-color 0.2s; }
        .input-wrapper:focus-within { border-color: var(--accent); }
        .input-wrapper svg { color: var(--text-placeholder); margin-right: 12px; }
        .input-wrapper input { background: transparent; border: none; padding: 14px 0; color: var(--text-primary); width: 100%; outline: none; font-size: 1rem; }

        .submit-btn { width: 100%; padding: 14px; background: var(--accent); border: none; border-radius: 12px; color: #000; font-weight: 700; font-size: 1rem; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 10px; margin-top: 10px; transition: transform 0.1s; }
        .submit-btn:active { transform: scale(0.98); }
        .submit-btn:disabled { opacity: 0.7; cursor: not-allowed; }

        .error-msg { background: rgba(239, 68, 68, 0.1); color: #ef4444; padding: 10px; border-radius: 8px; font-size: 0.9rem; display: flex; align-items: center; gap: 8px; margin-bottom: 20px; }

        .switch-text { margin-top: 24px; text-align: center; color: var(--text-secondary); font-size: 0.95rem; }
        .switch-text span { color: var(--accent); font-weight: 600; cursor: pointer; margin-left: 6px; }
        .switch-text span:hover { text-decoration: underline; }

        .spin { animation: spin 1s linear infinite; }
        @keyframes spin { 100% { transform: rotate(360deg); } }

        @media(max-width: 900px) {
            .auth-brand { display: none; }
        }
      `}</style>
        </div>
    );
};

export default AuthPage;
