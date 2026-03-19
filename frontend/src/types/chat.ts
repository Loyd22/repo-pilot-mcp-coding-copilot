export type ChatMessage = {
  id: string;
  role: "user" | "assistant";
  content: string;
};

export type ChatRequest = {
  repo_path: string;
  message: string;
};

export type ChatApiResponse = {
  success: boolean;
  user_message: string;
  intent: string;
  answer: string;
};