import type { ChatMessage } from "../types/chat";

type MessageListProps = {
  messages: ChatMessage[];
};

function MessageList({ messages }: MessageListProps) {
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "12px", marginBottom: "16px" }}>
      {messages.map((message) => (
        <div
          key={message.id}
          style={{
            padding: "12px",
            borderRadius: "10px",
            backgroundColor: message.role === "user" ? "#dbeafe" : "#e5e7eb",
            alignSelf: message.role === "user" ? "flex-end" : "flex-start",
            maxWidth: "70%",
          }}
        >
          <strong>{message.role === "user" ? "You" : "Assistant"}:</strong>
          <div>{message.content}</div>
        </div>
      ))}
    </div>
  );
}

export default MessageList;