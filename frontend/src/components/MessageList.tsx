import EditProposalCard from "./EditProposalCard";
import type { ChatMessage } from "../types/chat";

// Props for this component
type MessageListProps = {
  messages: ChatMessage[];
};

function MessageList({ messages }: MessageListProps) {
  return (
    <div className="space-y-4">
      {messages.map((message) => (
        <div
          key={message.id}
          className={`rounded-2xl border p-4 ${
            message.role === "user"
              ? "border-sky-700 bg-sky-950/30"
              : "border-zinc-700 bg-zinc-900/60"
          }`}
        >
          {/* Message header */}
          <div className="mb-2 flex items-center gap-2">
            <span className="text-sm font-semibold text-white">
              {message.role === "user" ? "You" : "Repo Pilot"}
            </span>

            {/* Show the detected intent if available */}
            {message.role === "assistant" && message.intent && (
              <span className="rounded-full border border-zinc-600 px-2 py-0.5 text-[11px] uppercase tracking-wide text-zinc-300">
                {message.intent}
              </span>
            )}
          </div>

          {/* Main message content */}
          <pre className="whitespace-pre-wrap text-sm text-zinc-100">
            {message.content}
          </pre>

          {/* If the assistant returned an edit proposal, show the proposal card */}
          {message.role === "assistant" && message.editProposalId && (
            <EditProposalCard
              proposalId={message.editProposalId}
              initialStatus={message.editProposalStatus}
              initialSummary={message.editSummary}
            />
          )}
        </div>
      ))}
    </div>
  );
}

export default MessageList;