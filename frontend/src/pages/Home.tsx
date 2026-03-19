import { useMemo, useState } from "react";
import { apiClient } from "../api/client";
import ChatBox from "../components/ChatBox";
import InfoPanel from "../components/InfoPanel";
import MessageList from "../components/MessageList";
import type { ChatApiResponse, ChatMessage } from "../types/chat";

function Home() {
  const [sessionId, setSessionId] = useState("session-001");
  const [repoPath, setRepoPath] = useState(
    "C:/Users/Loyd/Desktop/AA_AI_Engineer_Project/repo-pilot-mcp-coding-copilot"
  );

  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: crypto.randomUUID(),
      role: "assistant",
      content:
        "Repo Pilot is ready.\n\nTry:\n- Explain this repo\n- Read backend/app/main.py\n- Find FastAPI\n- What changed?",
    },
  ]);

  const [isLoading, setIsLoading] = useState(false);

  const latestAssistantMessage = useMemo(() => {
    return [...messages].reverse().find((message) => message.role === "assistant");
  }, [messages]);

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
        session_id: sessionId,
        repo_path: repoPathValue,
        message,
      });

      const assistantMessage: ChatMessage = {
        id: crypto.randomUUID(),
        role: "assistant",
        content: response.data.answer,
        intent: response.data.intent,
        toolTrace: response.data.tool_trace,
        filesViewed: response.data.files_viewed,
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error: any) {
      const assistantMessage: ChatMessage = {
        id: crypto.randomUUID(),
        role: "assistant",
        content:
          error?.response?.data?.detail ||
          "Failed to connect to the chat endpoint.",
        intent: "error",
        toolTrace: [],
        filesViewed: [],
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="page-shell">
      <div className="page-container">
        <header className="hero-section">
          <p className="hero-badge">MCP Coding Copilot</p>
          <h1 className="hero-title">Repo Pilot</h1>
          <p className="hero-subtitle">
            A personal AI repo assistant for understanding codebases, searching files,
            reading source code, and reviewing development changes.
          </p>
        </header>

        <section className="workspace-grid">
          <div className="workspace-card main-workspace">
            <div className="workspace-header">
              <div>
                <h2 className="workspace-title">Assistant Workspace</h2>
                <p className="workspace-subtitle">
                  Chat with your repository using the workflow you built.
                </p>
              </div>
            </div>

            <div className="session-row">
              <div className="input-group">
                <label className="input-label">Session ID</label>
                <input
                  type="text"
                  value={sessionId}
                  onChange={(e) => setSessionId(e.target.value)}
                  className="text-input"
                  placeholder="Enter session ID..."
                />
              </div>
            </div>

            <MessageList messages={messages} />

            <ChatBox
              onSendMessage={handleSendMessage}
              isLoading={isLoading}
              repoPath={repoPath}
              setRepoPath={setRepoPath}
            />
          </div>

          <div className="sidebar-panels">
            <InfoPanel
              title="Tool Trace"
              items={latestAssistantMessage?.toolTrace ?? []}
              emptyText="No tool trace available yet."
            />

            <InfoPanel
              title="Files Viewed"
              items={latestAssistantMessage?.filesViewed ?? []}
              emptyText="No files viewed yet."
            />
          </div>
        </section>
      </div>
    </div>
  );
}

export default Home;