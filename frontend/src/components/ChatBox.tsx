import { useState } from "react";

type ChatBoxProps = {
  onSendMessage: (repoPath: string, message: string) => void;
  isLoading: boolean;
  repoPath: string;
  setRepoPath: (value: string) => void;
};

function ChatBox({ onSendMessage, isLoading, repoPath, setRepoPath }: ChatBoxProps) {
  const [input, setInput] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!input.trim() || !repoPath.trim() || isLoading) return;

    onSendMessage(repoPath.trim(), input.trim());
    setInput("");
  };

  return (
    <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
      <input
        type="text"
        value={repoPath}
        onChange={(e) => setRepoPath(e.target.value)}
        placeholder="Enter repo path..."
        style={{
          padding: "12px",
          borderRadius: "8px",
          border: "1px solid #ccc",
        }}
      />

      <div style={{ display: "flex", gap: "8px" }}>
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
      </div>
    </form>
  );
}

export default ChatBox;