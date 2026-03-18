import { useState } from "react";

type ChatBoxProps = {
  onSendMessage: (message: string) => void;
  isLoading: boolean;
};

function ChatBox({ onSendMessage, isLoading }: ChatBoxProps) {
  const [input, setInput] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!input.trim() || isLoading) return;

    onSendMessage(input.trim());
    setInput("");
  };

  return (
    <form onSubmit={handleSubmit} style={{ display: "flex", gap: "8px" }}>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Ask something..."
        style={{
          flex: 1,
          padding: "12px",
          borderRadius: "8px",
          border: "1px solid #ccc",
        }}
      />
      <button
        type="submit"
        disabled={isLoading}
        style={{
          padding: "12px 16px",
          borderRadius: "8px",
          border: "none",
          cursor: "pointer",
        }}
      >
        {isLoading ? "Sending..." : "Send"}
      </button>
    </form>
  );
}

export default ChatBox;