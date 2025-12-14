import React, { useState, useRef, useEffect } from "react";
import { Send, Mic, X, Globe, Paperclip, ChevronUp } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface Props {
  onSend: (text: string, image?: string, language?: string) => void;
  onStop?: () => void;
  isLoading?: boolean;
  startText?: string;
}

const LANGUAGES = [
  { code: "en", name: "English" },
  { code: "hi", name: "Hindi" },
  { code: "ta", name: "Tamil" },
  { code: "te", name: "Telugu" },
  { code: "ml", name: "Malayalam" },
  { code: "mr", name: "Marathi" },
  { code: "kn", name: "Kannada" },
  { code: "bn", name: "Bengali" },
  { code: "gu", name: "Gujarati" }
];

const Composer: React.FC<Props> = ({ onSend, onStop, isLoading, startText }) => {
  const [value, setValue] = useState("");
  const [selectedLanguage, setSelectedLanguage] = useState("en");
  const [isListening, setIsListening] = useState(false);
  const [image, setImage] = useState<string | null>(null);
  const [showLangMenu, setShowLangMenu] = useState(false);

  // Sync startText when it changes (for Edit feature)
  useEffect(() => {
    if (startText) {
      setValue(startText);
      if (textAreaRef.current) textAreaRef.current.focus();
    }
  }, [startText]);

  const fileInputRef = useRef<HTMLInputElement>(null);
  const textAreaRef = useRef<HTMLTextAreaElement>(null);
  const langMenuRef = useRef<HTMLDivElement>(null);



  useEffect(() => {
    // Auto-resize textarea
    if (textAreaRef.current) {
      textAreaRef.current.style.height = 'auto';
      textAreaRef.current.style.height = textAreaRef.current.scrollHeight + 'px';
    }
  }, [value]);

  // Click outside to close lang menu
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (langMenuRef.current && !langMenuRef.current.contains(event.target as Node)) {
        setShowLangMenu(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

  const toggleListening = async () => {
    if (isListening) {
      // Stop Recording
      if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
        mediaRecorderRef.current.stop();
        setIsListening(false);
      }
    } else {
      // Start Recording
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const mediaRecorder = new MediaRecorder(stream);
        mediaRecorderRef.current = mediaRecorder;
        audioChunksRef.current = [];

        mediaRecorder.ondataavailable = (event) => {
          if (event.data.size > 0) {
            audioChunksRef.current.push(event.data);
          }
        };

        mediaRecorder.onstop = async () => {
          const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
          // Send to backend
          const formData = new FormData();
          formData.append('file', audioBlob, 'voice.webm');

          try {
            const response = await fetch('http://localhost:8000/api/utils/transcribe', {
              method: 'POST',
              body: formData
            });
            if (response.ok) {
              const data = await response.json();

              // 1. Set Text
              if (data.text) {
                setValue(prev => prev + (prev ? " " : "") + data.text);
              }

              // 2. Set Language (Auto-switch)
              if (data.language) {
                const detected = data.language.toLowerCase();
                // Map common Groq/Whisper language names to our codes
                const langMap: { [key: string]: string } = {
                  "english": "en", "hindi": "hi", "tamil": "ta", "telugu": "te",
                  "malayalam": "ml", "marathi": "mr", "kannada": "kn",
                  "bengali": "bn", "gujarati": "gu"
                };
                const code = langMap[detected] || "en";
                setSelectedLanguage(code);
              }
            } else {
              console.error("Transcription failed");
            }
          } catch (err) {
            console.error("Error uploading audio", err);
          }

          // Stop tracks
          stream.getTracks().forEach(track => track.stop());
        };

        mediaRecorder.start();
        setIsListening(true);
      } catch (err) {
        console.error("Microphone access denied", err);
        alert("Microphone access required for voice input.");
      }
    }
  };

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      processFile(file);
    }
  };

  // Handle Paste
  const handlePaste = (e: React.ClipboardEvent) => {
    const items = e.clipboardData.items;
    for (let i = 0; i < items.length; i++) {
      if (items[i].type.indexOf('image') !== -1) {
        const file = items[i].getAsFile();
        if (file) processFile(file);
      }
    }
  };

  const processFile = (file: File) => {
    const reader = new FileReader();
    reader.onloadend = () => {
      setImage(reader.result as string);
    };
    reader.readAsDataURL(file);
  };

  const handleSend = () => {
    if ((!value.trim() && !image) || isLoading) return;

    // Always pass the selected language
    onSend(value, image || undefined, selectedLanguage);

    setValue("");
    setImage(null);
    if (textAreaRef.current) textAreaRef.current.style.height = 'auto';
  };

  const handleKeyDown: React.KeyboardEventHandler<HTMLTextAreaElement> = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const currentLangName = LANGUAGES.find(l => l.code === selectedLanguage)?.name || "English";

  /* India-Specific Cybercrime Templates */
  const QUICK_REPORTS = [
    { label: "💸 UPI Fraud", text: "I want to report a UPI fraud. I lost money by scanning a QR code / entering my PIN to 'receive' money." },
    { label: "👮 Fake Police Call", text: "I received a call from someone claiming to be Police/CBI saying my child is arrested or a parcel is seized. They demanded money." },
    { label: "📵 Lost/Stolen Phone", text: "My mobile phone has been lost/stolen. I want to report it and block the IMEI to prevent misuse." },
    { label: "👠 Job/Task Scam", text: "I was added to a Telegram/WhatsApp group promising payment for 'liking' videos or rating hotels. I invested money and now cannot withdraw." },
    { label: "💔 Sextortion", text: "I am being blackmailed with a morphed/private video after a video call from an unknown number. They are demanding money." },
    { label: "💳 Credit Card Fraud", text: "An unauthorized transaction happened on my Credit/Debit card. I did not share my OTP." },
    { label: "📉 Stock/Investment Scam", text: "I invested in a 'high return' stock trading group on WhatsApp requiring an app download. Now I can't withdraw my profits." },
    { label: "📦 Courier/FedEx Scam", text: "I got a call saying a parcel in my name contains illegal items (Drugs/Passport) and I must pay to avoid arrest." },
    { label: "👤 Social Media Impersonation", text: "Someone created a fake Instagram/Facebook profile using my photo and name, asking my friends for money." },
    { label: "🏚️ Electricity Bill Scam", text: "I got a message saying my electricity will be cut tonight unless I update my bill. They asked me to download 'TeamViewer/AnyDesk'." }
  ];

  return (
    <div className="composer-container">
      {/* Quick Suggestions Chips */}
      {!value && !image && (
        <div className="quick-suggestions">
          {QUICK_REPORTS.map((item) => (
            <button
              key={item.label}
              className="suggestion-chip"
              onClick={() => setValue(item.text)}
            >
              {item.label}
            </button>
          ))}
        </div>
      )}

      {image && (
        <div className="image-preview" style={{ marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '10px', background: 'var(--bg-hover)', padding: '8px', borderRadius: '8px' }}>
          <img src={image} alt="Prev" style={{ width: '40px', height: '40px', objectFit: 'cover', borderRadius: '4px' }} />
          <span style={{ fontSize: '12px', color: 'var(--text-secondary)', flex: 1 }}>File attached</span>
          <button onClick={() => setImage(null)} style={{ background: 'none', border: 'none', color: 'var(--text-primary)', cursor: 'pointer' }}>
            <X size={14} />
          </button>
        </div>
      )}

      <textarea
        ref={textAreaRef}
        className="composer-textarea"
        rows={1}
        placeholder="Ask anything... (Paste image supported)"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={handleKeyDown}
        onPaste={handlePaste}
        disabled={isLoading}
      />

      <div className="composer-bottom">
        <div className="action-row">
          {/* Custom Language Dropdown */}
          <div className="relative" ref={langMenuRef} style={{ position: 'relative' }}>
            <button
              className="lang-badge"
              onClick={() => setShowLangMenu(!showLangMenu)}
              title="Response Language"
              style={{ display: 'flex', alignItems: 'center', gap: '6px', background: 'var(--bg-card)', padding: '4px 8px', borderRadius: '4px', border: '1px solid var(--border)', color: 'var(--text-secondary)', fontSize: '12px', cursor: 'pointer' }}
            >
              <Globe size={14} />
              <span>{currentLangName}</span>
              <ChevronUp size={12} style={{ transform: showLangMenu ? 'rotate(180deg)' : 'rotate(0deg)', transition: '0.2s' }} />
            </button>

            <AnimatePresence>
              {showLangMenu && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: 10 }}
                  transition={{ duration: 0.15 }}
                  style={{
                    position: 'absolute',
                    bottom: '100%',
                    left: 0,
                    marginBottom: '8px',
                    background: 'var(--bg-card)',
                    border: '1px solid var(--border)',
                    borderRadius: '8px',
                    padding: '4px',
                    width: '120px',
                    zIndex: 50,
                    maxHeight: '200px',
                    overflowY: 'auto',
                    boxShadow: 'var(--shadow-card)'
                  }}
                >
                  {LANGUAGES.map(lang => (
                    <div
                      key={lang.code}
                      onClick={() => { setSelectedLanguage(lang.code); setShowLangMenu(false); }}
                      style={{
                        padding: '6px 8px',
                        fontSize: '12px',
                        color: selectedLanguage === lang.code ? 'var(--text-primary)' : 'var(--text-secondary)',
                        background: selectedLanguage === lang.code ? 'var(--bg-hover)' : 'transparent',
                        borderRadius: '4px',
                        cursor: 'pointer',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'space-between'
                      }}
                      onMouseEnter={(e) => e.currentTarget.style.background = 'rgba(255,255,255,0.05)'}
                      onMouseLeave={(e) => e.currentTarget.style.background = selectedLanguage === lang.code ? 'rgba(255,255,255,0.1)' : 'transparent'}
                    >
                      {lang.name}
                    </div>
                  ))}
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          <div style={{ width: '1px', height: '20px', background: '#333', margin: '0 4px' }}></div>

          <button className="action-btn" onClick={() => fileInputRef.current?.click()} title="Attach Image">
            <Paperclip size={18} />
          </button>
          <input type="file" ref={fileInputRef} hidden accept="image/*" onChange={handleImageUpload} />

          <button className={`action-btn ${isListening ? 'active' : ''}`} onClick={toggleListening} title="Voice Input">
            <Mic size={18} />
          </button>
        </div>

        <button
          className="submit-btn"
          onClick={isLoading ? onStop : handleSend}
          disabled={(!value.trim() && !image && !isLoading)}
          style={isLoading ? { background: '#ef4444' } : {}}
        >
          {isLoading ? (
            <div style={{ width: '12px', height: '12px', background: '#fff', borderRadius: '2px' }} />
          ) : (
            <Send size={16} />
          )}
        </button>
      </div>

      <style>{`
        @keyframes spin { 100% { transform: rotate(360deg); } }
        /* Scrollbar for lang menu */
        .lang-menu::-webkit-scrollbar { width: 4px; }
        .lang-menu::-webkit-scrollbar-track { background: transparent; }
        .lang-menu::-webkit-scrollbar-thumb { background: #475569; borderRadius: 2px; }

        .quick-suggestions { 
            display: flex; 
            gap: 8px; 
            overflow-x: auto; 
            padding-bottom: 8px; 
            margin-bottom: 8px; 
            width: 100%;
            mask-image: linear-gradient(to right, black 95%, transparent 100%);
            -webkit-mask-image: linear-gradient(to right, black 95%, transparent 100%);
        }
        
        /* Thin, dark scrollbar for suggestions */
        .quick-suggestions::-webkit-scrollbar { height: 4px; display: block; }
        .quick-suggestions::-webkit-scrollbar-track { background: transparent; }
        .quick-suggestions::-webkit-scrollbar-thumb { background: #444; borderRadius: 2px; }
        
        .suggestion-chip {
           background: var(--bg-hover); 
           border: 1px solid var(--border); 
           color: var(--text-secondary); 
           padding: 6px 14px; 
           border-radius: 20px; 
           font-size: 13px; 
           white-space: nowrap; 
           cursor: pointer; 
           transition: all 0.2s;
           flex-shrink: 0;
           display: flex;
           align-items: center;
        }
        .suggestion-chip:hover { background: var(--bg-card); color: var(--text-primary); border-color: var(--accent); }
       `}</style>
    </div>
  );
};

export default Composer;
