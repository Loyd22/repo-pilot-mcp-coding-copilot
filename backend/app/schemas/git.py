"""
Schemas for git-related endpoints.
"""

from pydantic import BaseModel, Field


class GitDiffRequest(BaseModel):
    """Request schema for reading git diff."""

    repo_path: str = Field(..., min_length=1, description="Absolute path to the repository")


class GitDiffData(BaseModel):
    """Data returned for git diff."""

    changed_files: list[str]
    diff: str


class GitDiffResponse(BaseModel):
    """Response schema for git diff endpoint."""

    success: bool
    data: GitDiffData