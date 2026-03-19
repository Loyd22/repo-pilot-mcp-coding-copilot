import { useState } from "react";
import { apiClient } from "../api/client";
import ChatBox from "../components/ChatBox";
import MessageList from "../components/MessageList";
import type { ChatApiResponse, ChatMessage } from "../types/chat";

function Home() {
  const [repoPath, setRepoPath] = useState(
    "C:/Users/Loyd/Desktop/AA_AI_Engineer_Project/repo-pilot-mcp-coding-copilot"
  );

  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: crypto.randomUUID(),
      role: "assistant",
      content: "Repo Pilot is ready. Enter your repo path and ask a question.",
    },
  ]);

  const [isLoading, setIsLoading] = useState(false);

  const handleSendMessage = async (repoPathValue: string, message: string) => {
    const userMessage: ChatMessage = {
      id: crypto.randomUUID(),
      role: "user",
      content: message,
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await apiClient.post<ChatApiResponse>("/api/v1/chat", {
        repo_path: repoPathValue,
        message,
      });

      const assistantMessage: ChatMessage = {
        id: crypto.randomUUID(),
        role: "assistant",
        content: response.data.answer,
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error: any) {
      const assistantMessage: ChatMessage = {
        id: crypto.randomUUID(),
        role: "assistant",
        content:
          error?.response?.data?.detail ||
          "Failed to connect to chat endpoint.",
      };

      setMessages((prev) => [...prev, assistantMessage]);
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
          gap: "16px",
        }}
      >
        <MessageList messages={messages} />
        <ChatBox
          onSendMessage={handleSendMessage}
          isLoading={isLoading}
          repoPath={repoPath}
          setRepoPath={setRepoPath}
        />
      </div>
    </div>
  );
}

export default Home;