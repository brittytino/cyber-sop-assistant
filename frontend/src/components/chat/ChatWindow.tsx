import React, { useState, useRef, useEffect } from "react";
import Composer from "./Composer";
import { Menu, Pencil } from "lucide-react";
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { chatAPI } from '../../api/client';

interface Msg {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  sources?: any[];
  image?: string;
}

interface ChatWindowProps {
  setIsMobileOpen?: (open: boolean) => void;
  activeChatId?: number | null;
  setActiveChatId?: (id: number) => void;
}

const ChatWindow: React.FC<ChatWindowProps> = ({
  setIsMobileOpen,
  activeChatId,
  setActiveChatId = () => { }
}) => {
  const [messages, setMessages] = useState<Msg[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [editDraft, setEditDraft] = useState<string>("");
  const creationIdRef = useRef<number | null>(null);
  const abortControllerRef = useRef<AbortController | null>(null);

  // If we have an active ID, we are in "chat" mode. If not, and no local messages, "home".
  const viewMode = (activeChatId || messages.length > 0) ? 'chat' : 'home';

  // Load chat history when activeChatId changes
  useEffect(() => {
    if (activeChatId) {
      // If this ID matches the one we just created in the current session, don't reload history
      // (preserves the optimistic state and stream)
      if (activeChatId === creationIdRef.current) {
        creationIdRef.current = null; // Reset
        return;
      }
      loadChatHistory(activeChatId);
    } else {
      setMessages([]); // Clear for new chat
    }
  }, [activeChatId]);

  // Force new thread on component mount if no ID is provided (Ensure "Home" state)
  useEffect(() => {
    if (!activeChatId) {
      setMessages([]);
      creationIdRef.current = null;
    }
  }, []);

  const loadChatHistory = async (id: number) => {
    try {
      setIsLoading(true);
      const chat = await chatAPI.getChat(id);
      if (chat && chat.messages) {
        setMessages(chat.messages.map((m: any) => ({
          id: m.id.toString(),
          role: m.role,
          content: m.content,
          image: m.image
        })));
      }
    } catch (err) {
      console.error("Failed to load history", err);
    } finally {
      setIsLoading(false);
    }
  };

  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);


  const handleStop = () => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      setIsLoading(false);
      abortControllerRef.current = null;
    }
  };

  const handleEdit = (text: string) => {
    setEditDraft(text);
  };

  const handleSend = async (text: string, image?: string, language?: string) => {
    if (!text && !image) return;

    // Clear draft if it was an edit
    setEditDraft("");

    const displayContent = text || (image ? "Analyzed uploaded image" : "");

    // Optimistic User Message
    const userMsg: Msg = {
      id: Date.now().toString(),
      role: 'user',
      content: displayContent,
      image: image
    };

    setMessages(prev => [...prev, userMsg]);
    setIsLoading(true);
    setError(null);

    try {
      // Placeholder Assistant Message
      const assistantMsgId = (Date.now() + 1).toString();
      const assistantMsg: Msg = { id: assistantMsgId, role: 'assistant', content: '', sources: [] };
      setMessages(prev => [...prev, assistantMsg]);

      const body: any = { message: text || "Analyze this image" };
      if (image) body.image = image;
      if (language) body.language = language;
      if (activeChatId) body.chat_id = activeChatId; // Append to existing chat

      const token = localStorage.getItem('cyber_sop_token');

      const controller = new AbortController();
      abortControllerRef.current = controller;

      const response = await fetch('http://localhost:8000/api/chat/message', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(body),
        signal: controller.signal
      });

      if (!response.ok) throw new Error('Network response was not ok');
      const reader = response.body?.getReader();
      if (!reader) throw new Error('No reader available');

      const decoder = new TextDecoder();
      let accumulatedContent = '';
      let sources: any[] = [];
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';

        for (const line of lines) {
          if (!line.trim()) continue;
          try {
            const data = JSON.parse(line);

            if (data.type === 'meta') {
              // CAPTURE NEW CHAT ID
              if (data.chat_id && data.chat_id !== activeChatId) {
                creationIdRef.current = data.chat_id; // MARK AS CREATED BY THIS SESSION
                setActiveChatId(data.chat_id);
              }
            } else if (data.type === 'content') {
              accumulatedContent += data.data;
              setMessages(prev =>
                prev.map(m => m.id === assistantMsgId ? { ...m, content: accumulatedContent } : m)
              );
            } else if (data.type === 'sources') {
              sources = data.data;
              setMessages(prev =>
                prev.map(m => m.id === assistantMsgId ? { ...m, sources: sources } : m)
              );
            } else if (data.type === 'error') {
              setError(data.error);
            }
          } catch (e) {
            console.error('Error parsing chunk', e);
          }
        }
      }

    } catch (err: any) {
      setError(err.message || "Failed to send message");
    } finally {
      setIsLoading(false);
      abortControllerRef.current = null;
    }
  };

  const MarkdownRenderer = ({ content }: { content: string }) => (
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      components={{
        // Style custom headers
        h1: ({ node, ...props }) => <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginTop: '1rem', marginBottom: '0.5rem' }} {...props} />,
        h2: ({ node, ...props }) => <h4 style={{ fontSize: '1rem', fontWeight: 600, marginTop: '0.8rem', marginBottom: '0.4rem' }} {...props} />,
        h3: ({ node, ...props }) => <strong style={{ display: 'block', marginTop: '0.5rem' }} {...props} />,
        p: ({ node, ...props }) => <p style={{ margin: '0 0 0.8rem 0', lineHeight: 1.6 }} {...props} />,
        ul: ({ node, ...props }) => <ul style={{ paddingLeft: '1.2rem', margin: '0.5rem 0' }} {...props} />,
        li: ({ node, ...props }) => <li style={{ marginBottom: '0.25rem' }} {...props} />,
        code: ({ node, ...props }) => <code style={{ background: 'rgba(255,255,255,0.1)', padding: '2px 4px', borderRadius: '4px', fontSize: '0.9em' }} {...props} />,
        a: ({ node, ...props }) => <a style={{ color: 'var(--accent)', textDecoration: 'none' }} target="_blank" rel="noopener noreferrer" {...props} />
      }}
    >
      {content}
    </ReactMarkdown>
  );

  return (
    <div className={`chat-window ${viewMode}`}>
      {/* Mobile Header */}
      <div className="mobile-header">
        <button onClick={() => setIsMobileOpen && setIsMobileOpen(true)} style={{ background: 'none', border: 'none', color: '#fff' }}>
          <Menu size={24} />
        </button>
        <span style={{ marginLeft: '12px', fontWeight: 600 }}>Cyber SOP</span>
      </div>

      {viewMode === 'home' ? (
        <div className="home-content">
          <div className="perplexity-logo-large" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '8px' }}>
            <span style={{ fontSize: '3rem', color: '#f97316' }}>✶</span>
            <span>Cyber SOP Assistant</span>
            <span style={{ fontSize: '1rem', color: '#888', fontWeight: 400, marginTop: '-10px' }}>Verify. Report. Stay Safe.</span>
          </div>
          <div style={{ width: '100%' }}>
            <Composer onSend={handleSend} onStop={handleStop} isLoading={isLoading} startText={editDraft} />
          </div>

          {/* Disclaimer/Footer - Relatable Content */}
          <div style={{ display: 'flex', gap: '20px', fontSize: '12px', color: '#666', marginTop: 'auto' }}>
            <a href="https://cybercrime.gov.in" target="_blank" rel="noopener noreferrer" style={{ color: 'inherit', textDecoration: 'none' }}>National Portal</a>
            <span>•</span>
            <span style={{ color: '#f97316', fontWeight: 600 }}>Helpline 1930</span>
            <span>•</span>
            <span>Safe Browsing</span>
            <span>•</span>
            <span>Privacy</span>
          </div>
        </div>
      ) : (
        /* Chat Mode */
        <>
          <div className="messages-area">
            <div className="messages-wrapper">
              {messages.map((m) => (
                <div key={m.id} className="message-block">
                  <div className="message-header">
                    <div className={`avatar ${m.role === 'user' ? 'user' : 'ai'}`}>
                      {m.role === 'user' ? 'U' : '✶'}
                    </div>
                    <span>{m.role === 'user' ? 'You' : 'Cyber SOP'}</span>

                    {/* Rewrite Button for User */}
                    {m.role === 'user' && !isLoading && (
                      <button
                        onClick={() => handleEdit(m.content)}
                        title="Edit and Resend"
                        style={{ background: 'none', border: 'none', color: '#666', cursor: 'pointer', marginLeft: '10px' }}
                      >
                        <Pencil size={12} />
                      </button>
                    )}
                  </div>

                  {m.image && m.role === 'user' && (
                    <div style={{ marginLeft: '40px', marginBottom: '10px' }}>
                      <img src={m.image} alt="Upload" style={{ maxHeight: '200px', borderRadius: '8px', border: '1px solid #333' }} />
                    </div>
                  )}

                  <div className="message-content">
                    {m.role === 'assistant' ? (
                      m.content ? (
                        <MarkdownRenderer content={m.content} />
                      ) : (
                        isLoading && <span style={{ color: 'var(--accent)' }}>Thinking...</span>
                      )
                    ) : (
                      <p>{m.content}</p>
                    )}
                  </div>

                  {m.sources && m.sources.length > 0 && (
                    <div className="sources-grid">
                      {m.sources.map((s: any, i: number) => (
                        <div className="source-card" key={i} title={s.content}>
                          <div className="source-title">{s.source}</div>
                          <div className="source-meta">{s.metadata?.section || 'Reference'}</div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              ))}
              {error && (
                <div style={{ color: '#ea580c', textAlign: 'center', padding: '10px' }}>
                  Error: {error}
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
          </div>

          <div className="composer-wrapper">
            <Composer onSend={handleSend} onStop={handleStop} isLoading={isLoading} startText={editDraft} />
          </div>
        </>
      )}
    </div>
  );
};

export default ChatWindow;
