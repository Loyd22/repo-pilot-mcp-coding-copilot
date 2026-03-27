"""
This file defines the input and output shape of the chat API.

Simple meaning:
- ChatRequest = what the frontend sends to backend
- ChatResponse = what the backend sends back to frontend
"""

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Request body for the chat endpoint."""

    # Unique chat session
    session_id: str = Field(..., min_length=1, description="Chat session ID")

    # Which repository the assistant should work on
    repo_path: str = Field(..., min_length=1, description="Absolute path to the repository")

    # The user's chat message
    message: str = Field(..., min_length=1, description="User chat message")


class ChatResponse(BaseModel):
    """Response body returned by the chat endpoint."""

    # Whether the request succeeded
    success: bool

    # Session info
    session_id: str

    # The original user message
    user_message: str

    # What kind of request the system detected
    intent: str

    # Final answer shown in the UI
    answer: str

    # Step-by-step trace of what the workflow did
    tool_trace: list[str]

    # Which files were involved
    files_viewed: list[str]

    # Phase 8 fields for safe edit mode
    edit_proposal_id: int | None = None
    edit_proposal_status: str | None = None
    edit_summary: str | None = None


    verification_summary: str | None = None
    verification_results: list[dict] | None = None