// This component is the message input box at the bottom of the chat.
//
// Simple meaning:
// - The user types a message here
// - When the user clicks send, it calls the parent function
// - This component does NOT manage the repo path input
// - The repo path is already handled in Home.tsx

import { useState } from "react";

// These are the props this component needs from Home.tsx
type ChatBoxProps = {
  // Current repository path, passed from the parent
  repoPath: string;

  // Function to send the user's message to the backend
  onSendMessage: (repoPathValue: string, message: string) => Promise<void>;

  // True while waiting for backend response
  isLoading: boolean;
};

function ChatBox({ onSendMessage, isLoading, repoPath }: ChatBoxProps) {
  // Local state for the text inside the message input box
  const [message, setMessage] = useState("");

  // This function runs when the user clicks Send
  const handleSend = async () => {
    // Stop if message is empty
    if (!message.trim()) return;

    // Send the message to the parent component
    await onSendMessage(repoPath, message);

    // Clear the input after sending
    setMessage("");
  };

  return (
    <div className="flex items-center gap-3">
      {/* Message input box */}
      <input
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Ask something..."
        className="flex-1 rounded-xl border border-zinc-700 bg-zinc-900 px-4 py-3 text-sm text-white"
        disabled={isLoading}
      />

      {/* Send button */}
      <button
        onClick={handleSend}
        disabled={isLoading || !message.trim()}
        className="rounded-xl border border-zinc-700 bg-zinc-800 px-4 py-3 text-sm text-white hover:bg-zinc-700 disabled:opacity-50"
      >
        {isLoading ? "Sending..." : "Send"}
      </button>
    </div>
  );
}

export default ChatBox;