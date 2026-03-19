"""
Schemas for chat endpoint.
"""

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Request schema for chat endpoint."""



    session_id: str = Field(..., min_length=1, description="Chat session ID")
    repo_path: str = Field(..., min_length=1, description="Absolute path to the repository")
    message: str = Field(..., min_length=1, description="User chat message")


class ChatResponse(BaseModel):
    """Response schema for chat endpoint."""

    success: bool
    session_id: str
    user_message: str
    intent: str
    answer: str
    tool_trace: list[str]
    files_viewed: list[str]