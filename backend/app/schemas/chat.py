"""
Schemas for chat endpoint.
"""

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Request schema for chat endpoint."""

    repo_path: str = Field(..., min_length=1, description="Absolute path to the repository")
    message: str = Field(..., min_length=1, description="User chat message")


class ChatResponse(BaseModel):
    """Response schema for chat endpoint."""

    success: bool
    user_message: str
    intent: str
    answer: str