// This file defines the shapes of data used by the frontend.
//
// Simple meaning:
// - It tells TypeScript what a chat message looks like
// - It tells TypeScript what the backend response looks like
// - It also defines the new Phase 8 safe edit proposal data

export type ChatMessage = {
  // Unique ID used by React when showing messages
  id: string;

  // Who sent the message
  role: "user" | "assistant";

  // The actual text shown in chat
  content: string;

  // Optional backend metadata
  intent?: string;
  toolTrace?: string[];
  filesViewed?: string[];

  // New Phase 8 fields for safe edit mode
  editProposalId?: number;
  editProposalStatus?: string;
  editSummary?: string;
};

export type ChatRequest = {
  // Chat session ID
  session_id: string;

  // Which repo the assistant should work on
  repo_path: string;

  // User's message
  message: string;
};

export type ChatApiResponse = {
  // Whether the request succeeded
  success: boolean;

  // Session ID
  session_id: string;

  // Original user message
  user_message: string;

  // Detected intent from backend
  intent: string;

  // Final assistant answer
  answer: string;

  // Step-by-step workflow trace
  tool_trace: string[];

  // Files involved in the request
  files_viewed: string[];

  // New Phase 8 proposal info
  edit_proposal_id?: number | null;
  edit_proposal_status?: string | null;
  edit_summary?: string | null;
};

export type EditProposalFile = {
  // Which file will be changed
  file_path: string;

  // Type of change, such as create or update
  change_type: string;

  // File content before the change
  before_content: string;

  // File content after the change
  after_content: string;

  // Diff text for review
  diff_text: string;
};

export type EditProposalData = {
  // Proposal ID from backend
  id: number;

  // Related chat session
  session_id: string;

  // Repo path
  repo_path: string;

  // Original user request
  user_request: string;

  // Proposal title
  title: string;

  // Proposal summary
  summary: string;

  // Proposal status: proposed, approved, applied, etc.
  status: string;

  // Files inside this proposal
  files: EditProposalFile[];
};

export type EditProposalResponse = {
  // Whether fetch succeeded
  success: boolean;

  // Full proposal data
  data: EditProposalData;
};

export type EditActionResponse = {
  // Whether action succeeded
  success: boolean;

  // Proposal ID affected
  proposal_id: number;

  // New status after the action
  status: string;

  // Human-readable message
  message: string;
};