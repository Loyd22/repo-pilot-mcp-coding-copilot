export type ChatMessage = {
  id: string;
  role: "user" | "assistant";
  content: string;
  intent?: string;
  toolTrace?: string[];
  filesViewed?: string[];
};

export type ChatRequest = {
  session_id: string;
  repo_path: string;
  message: string;
};

export type ChatApiResponse = {
  success: boolean;
  session_id: string;
  user_message: string;
  intent: string;
  answer: string;
  tool_trace: string[];
  files_viewed: string[];
};