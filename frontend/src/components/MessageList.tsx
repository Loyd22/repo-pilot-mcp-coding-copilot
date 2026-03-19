import type { ChatMessage } from "../types/chat";

type MessageListProps = {
  messages: ChatMessage[];
};

function MessageList({ messages }: MessageListProps) {
  return (
    <div className="message-list">
      {messages.map((message) => (
        <div
          key={message.id}
          className={`message-row ${message.role === "user" ? "user-row" : "assistant-row"}`}
        >
          <div className={`message-card ${message.role === "user" ? "user-card" : "assistant-card"}`}>
            <div className="message-header">
              <span className="message-role">
                {message.role === "user" ? "You" : "Repo Pilot"}
              </span>

              {message.role === "assistant" && message.intent && (
                <span className="message-intent">{message.intent}</span>
              )}
            </div>

            <pre className="message-content">{message.content}</pre>
          </div>
        </div>
      ))}
    </div>
  );
}

export default MessageList;