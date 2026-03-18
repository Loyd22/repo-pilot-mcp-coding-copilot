import { useState } from "react";
import { apiClient } from "../api/client";
import ChatBox from "../components/ChatBox";
import MessageList from "../components/MessageList";
import type { ChatMessage } from "../types/chat";

function Home() {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: crypto.randomUUID(),
      role: "assistant",
      content: "Repo Pilot frontend is ready.",
    },
  ]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSendMessage = async (message: string) => {
    const userMessage: ChatMessage = {
      id: crypto.randomUUID(),
      role: "user",
      content: message,
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await apiClient.get("/");

      const assistantMessage: ChatMessage = {
        id: crypto.randomUUID(),
        role: "assistant",
        content: response.data.message || "No response from backend.",
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage: ChatMessage = {
        id: crypto.randomUUID(),
        role: "assistant",
        content: "Failed to connect to backend.",
      };

      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div
      style={{
        maxWidth: "900px",
        margin: "0 auto",
        padding: "40px 20px",
        fontFamily: "Arial, sans-serif",
      }}
    >
      <h1>Repo Pilot MCP Coding Copilot</h1>
      <p>Personal AI repo assistant for daily development workflow.</p>

      <div
        style={{
          marginTop: "24px",
          border: "1px solid #ddd",
          borderRadius: "12px",
          padding: "20px",
          minHeight: "500px",
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
        }}
      >
        <MessageList messages={messages} />
        <ChatBox onSendMessage={handleSendMessage} isLoading={isLoading} />
      </div>
    </div>
  );
}

export default Home;