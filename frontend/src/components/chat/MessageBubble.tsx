import React from "react";


interface Source {
  id: string;
  source: string;
  content: string;
}


interface Props {
  role: "user" | "assistant";
  content: string;
  sources?: Source[];
  image?: string;
}



const MessageBubble: React.FC<Props> = ({ role, content, sources, image }) => {
  const isUser = role === "user";
  return (
    <div
      className={`message-row ${isUser ? "user" : "assistant"}`}
    >
      <div className="message-bubble">
        <div className="message-role">
          {isUser ? "You" : "Assistant"}
        </div>

        {image && (
          <div className="message-image" style={{ marginBottom: '10px' }}>
            <img src={image} alt="User upload" style={{ maxWidth: '100%', borderRadius: '8px', maxHeight: '300px' }} />
          </div>
        )}

        <div className="message-content">
          {content.split('\n').map((line, i) => (
            <div key={i}>{line}</div>
          ))}
        </div>

        {sources && sources.length > 0 && (
          <div className="message-sources">
            <div style={{ fontSize: '11px', fontWeight: 600, color: '#94a3b8', marginBottom: '4px' }}>
              SOURCES
            </div>
            {sources.map((source, idx) => (
              <div key={idx} className="source-item">
                {source.source}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};


export default MessageBubble;
