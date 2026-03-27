import { useState } from "react";
import { apiClient } from "../api/client";
import type {
  EditActionResponse,
  EditProposalData,
  EditProposalResponse,
} from "../types/chat";

// Props are the input values this component needs from the parent
type EditProposalCardProps = {
  proposalId: number;
  initialStatus?: string;
  initialSummary?: string;
};

function EditProposalCard({
  proposalId,
  initialStatus = "proposed",
  initialSummary = "Review this proposal before applying.",
}: EditProposalCardProps) {
  // Stores the full proposal after fetching it from the backend
  const [proposal, setProposal] = useState<EditProposalData | null>(null);

  // Stores the current status shown in the UI
  const [status, setStatus] = useState(initialStatus);

  // Stores the summary shown before we load the full proposal
  const [summary, setSummary] = useState(initialSummary);

  // Used to disable buttons while waiting for the backend
  const [isLoading, setIsLoading] = useState(false);

  // Used to show errors in the UI
  const [errorMessage, setErrorMessage] = useState("");

  // Load the full proposal from the backend
  const loadProposal = async () => {
    setIsLoading(true);
    setErrorMessage("");

    try {
      const response = await apiClient.get<EditProposalResponse>(
        `/api/v1/edit/${proposalId}`
      );

      setProposal(response.data.data);
      setStatus(response.data.data.status);
      setSummary(response.data.data.summary);
    } catch (error: any) {
      setErrorMessage(
        error?.response?.data?.detail || "Failed to load proposal."
      );
    } finally {
      setIsLoading(false);
    }
  };

  // Approve, reject, or apply the proposal
  const runAction = async (action: "approve" | "reject" | "apply") => {
    setIsLoading(true);
    setErrorMessage("");

    try {
      const response = await apiClient.post<EditActionResponse>(
        `/api/v1/edit/${proposalId}/${action}`
      );

      // Update local status immediately
      setStatus(response.data.status);

      // Reload full proposal after the action
      await loadProposal();
    } catch (error: any) {
      setErrorMessage(
        error?.response?.data?.detail || `Failed to ${action} proposal.`
      );
      setIsLoading(false);
    }
  };

  return (
    <div className="mt-3 rounded-2xl border border-zinc-700 bg-zinc-900/70 p-4">
      {/* Top header of the proposal card */}
      <div className="mb-2 flex items-center justify-between">
        <div>
          <div className="text-sm font-semibold text-white">
            Safe Edit Proposal #{proposalId}
          </div>
          <div className="text-xs text-zinc-400">Status: {status}</div>
        </div>

        {/* Button to fetch and show full proposal details */}
        <button
          onClick={loadProposal}
          disabled={isLoading}
          className="rounded-lg border border-zinc-600 px-3 py-1 text-xs text-zinc-200 hover:bg-zinc-800 disabled:opacity-50"
        >
          Review
        </button>
      </div>

      {/* Small summary text */}
      <p className="text-sm text-zinc-300">{summary}</p>

      {/* Error box */}
      {errorMessage && (
        <div className="mt-3 rounded-lg border border-red-700 bg-red-950/40 p-2 text-xs text-red-300">
          {errorMessage}
        </div>
      )}

      {/* Only show this area after the user clicks Review and proposal is loaded */}
      {proposal && (
        <div className="mt-4 space-y-4">
          <div>
            <div className="text-sm font-medium text-white">
              {proposal.title}
            </div>
            <div className="text-xs text-zinc-400">{proposal.user_request}</div>
          </div>

          {/* Show all files included in the proposal */}
          <div className="space-y-3">
            {proposal.files.map((file) => (
              <div
                key={file.file_path}
                className="rounded-xl border border-zinc-700 bg-zinc-950/70 p-3"
              >
                <div className="mb-1 text-sm font-medium text-zinc-100">
                  {file.file_path}
                </div>
                <div className="mb-2 text-xs uppercase tracking-wide text-zinc-400">
                  {file.change_type}
                </div>

                {/* Show the diff text so the user can review changes */}
                <pre className="max-h-64 overflow-auto rounded-lg bg-black/50 p-3 text-xs text-zinc-200 whitespace-pre-wrap">
                  {file.diff_text || "No diff available."}
                </pre>
              </div>
            ))}
          </div>

          {/* Action buttons */}
          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => runAction("approve")}
              disabled={isLoading || status === "applied"}
              className="rounded-lg border border-emerald-700 px-3 py-2 text-xs text-emerald-300 hover:bg-emerald-950/40 disabled:opacity-50"
            >
              Approve
            </button>

            <button
              onClick={() => runAction("reject")}
              disabled={isLoading || status === "applied"}
              className="rounded-lg border border-amber-700 px-3 py-2 text-xs text-amber-300 hover:bg-amber-950/40 disabled:opacity-50"
            >
              Reject
            </button>

            <button
              onClick={() => runAction("apply")}
              disabled={isLoading || status !== "approved"}
              className="rounded-lg border border-sky-700 px-3 py-2 text-xs text-sky-300 hover:bg-sky-950/40 disabled:opacity-50"
            >
              Apply
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default EditProposalCard;