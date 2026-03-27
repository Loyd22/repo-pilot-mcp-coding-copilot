"""
Schemas for safe edit proposal endpoints.
"""

from pydantic import BaseModel, Field


class EditProposalRequest(BaseModel):
    """Request schema for creating an edit proposal."""

    session_id: str = Field(..., min_length=1, description="Chat session ID")
    repo_path: str = Field(..., min_length=1, description="Absolute path to the repository")
    message: str = Field(..., min_length=1, description="User request for code changes")


class EditProposalFileSchema(BaseModel):
    """Represents one proposed file change."""

    file_path: str
    change_type: str
    before_content: str
    after_content: str
    diff_text: str


class EditProposalData(BaseModel):
    """Payload for a full edit proposal."""

    id: int
    session_id: str
    repo_path: str
    user_request: str
    title: str
    summary: str
    status: str
    files: list[EditProposalFileSchema]


class EditProposalResponse(BaseModel):
    """Response schema for returning a full edit proposal."""

    success: bool
    data: EditProposalData


class EditActionResponse(BaseModel):
    """Simple response for approve/reject/apply actions."""

    success: bool
    proposal_id: int
    status: str
    message: str