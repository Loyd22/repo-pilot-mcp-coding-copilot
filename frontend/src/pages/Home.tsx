// This file is the main page of the frontend.
//
// Simple meaning:
// - It shows the chat UI
// - It sends messages to the FastAPI backend
// - It stores chat messages in local state
// - It shows the right-side info panels
// - It keeps Phase 8 proposal metadata from the backend response

import { useMemo, useState } from "react";
import { apiClient } from "../api/client";
import ChatBox from "../components/ChatBox";
import InfoPanel from "../components/InfoPanel";
import MessageList from "../components/MessageList";
import type { ChatApiResponse, ChatMessage } from "../types/chat";

function Home() {
  // This is the chat session ID.
  // It helps the backend remember the conversation history.
  const [sessionId, setSessionId] = useState("session-001");

  // This is the repository path that the backend will scan/analyze.
  const [repoPath, setRepoPath] = useState(
    "C:/Users/Loyd/Desktop/AA_AI_Engineer_Project/repo-pilot-mcp-coding-copilot"
  );

  // This stores all chat messages shown in the UI.
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: crypto.randomUUID(),
      role: "assistant",
      content:
        "Repo Pilot is ready.\n\nTry:\n- Explain this repo\n- Read backend/app/main.py\n- Find FastAPI\n- What changed?\n- Create a new file backend/test_phase8_output.py",
    },
  ]);

  // This is used to disable the send button while waiting for backend response.
  const [isLoading, setIsLoading] = useState(false);

  // This finds the most recent assistant message.
  // We use it for the right-side info panels.
  const latestAssistantMessage = useMemo(() => {
    return [...messages].reverse().find((message) => message.role === "assistant");
  }, [messages]);

  // This function runs when the user sends a message.
  const handleSendMessage = async (repoPathValue: string, message: string) => {
    // First, immediately show the user's message in the chat UI.
    const userMessage: ChatMessage = {
      id: crypto.randomUUID(),
      role: "user",
      content: message,
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      // Send the message to the backend chat endpoint.
      const response = await apiClient.post<ChatApiResponse>("/api/v1/chat", {
        session_id: sessionId,
        repo_path: repoPathValue,
        message,
      });

      // Build the assistant message using the backend response.
      // This includes normal chat fields and Phase 8 proposal fields.
      const assistantMessage: ChatMessage = {
        id: crypto.randomUUID(),
        role: "assistant",
        content: response.data.answer,
        intent: response.data.intent,
        toolTrace: response.data.tool_trace,
        filesViewed: response.data.files_viewed,
        editProposalId: response.data.edit_proposal_id ?? undefined,
        editProposalStatus: response.data.edit_proposal_status ?? undefined,
        editSummary: response.data.edit_summary ?? undefined,
      };

      // Add the assistant reply to the chat list.
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error: any) {
      // If something fails, show the error as an assistant message.
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
      // Re-enable the UI after request completes.
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-zinc-950 text-white">
      <div className="mx-auto max-w-7xl p-6">
        {/* Top page header */}
        <div className="mb-6">
          <div className="text-xs uppercase tracking-[0.2em] text-zinc-400">
            MCP Coding Copilot
          </div>

          <h1 className="mt-2 text-3xl font-bold">Repo Pilot</h1>

          <p className="mt-2 max-w-3xl text-zinc-300">
            A personal AI repo assistant for understanding codebases, searching files,
            reading source code, reviewing development changes, and safely proposing edits.
          </p>
        </div>

        {/* Inputs for session ID and repo path */}
        <div className="mb-4 grid gap-3 md:grid-cols-2">
          <input
            value={sessionId}
            onChange={(e) => setSessionId(e.target.value)}
            className="rounded-xl border border-zinc-700 bg-zinc-900 px-4 py-3 text-sm text-white"
            placeholder="Enter session ID..."
          />

          <input
            value={repoPath}
            onChange={(e) => setRepoPath(e.target.value)}
            className="rounded-xl border border-zinc-700 bg-zinc-900 px-4 py-3 text-sm text-white"
            placeholder="Enter repository path..."
          />
        </div>

        {/* Main layout:
            Left side = chat area
            Right side = metadata panels */}
        <div className="grid gap-6 lg:grid-cols-[1.5fr_0.8fr]">
          {/* Left side: main assistant workspace */}
          <div className="rounded-3xl border border-zinc-800 bg-zinc-900/40 p-5">
            <div className="mb-4">
              <h2 className="text-lg font-semibold">Assistant Workspace</h2>
              <p className="text-sm text-zinc-400">
                Chat with your repository using the workflow you built.
              </p>
            </div>

            {/* Chat messages area */}
            <MessageList messages={messages} />

            {/* Chat input area */}
            <div className="mt-5">
              <ChatBox
                repoPath={repoPath}
                onSendMessage={handleSendMessage}
                isLoading={isLoading}
              />
            </div>
          </div>

          {/* Right side: metadata/info panels
              We use the same InfoPanel component twice.
              One shows tool trace.
              One shows files viewed. */}
          <div className="space-y-6">
            <InfoPanel
              title="Tool Trace"
              items={latestAssistantMessage?.toolTrace || []}
              emptyText="No tool trace yet."
            />

            <InfoPanel
              title="Files Viewed"
              items={latestAssistantMessage?.filesViewed || []}
              emptyText="No files viewed yet."
            />
          </div>
        </div>
      </div>
    </div>
  );
}

export default Home;