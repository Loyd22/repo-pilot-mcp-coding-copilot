"""
Schemas for repo-related endpoints.
"""

from pydantic import BaseModel, Field


class RepoTreeRequest(BaseModel):
    """Request schema for scanning a repository tree."""

    repo_path: str = Field(..., min_length=1, description="Absolute path to the repository")


class RepoTreeData(BaseModel):
    """Data returned for a repository tree scan."""

    repo_name: str
    tree: list[str]


class RepoTreeResponse(BaseModel):
    """Response schema for repository tree scan."""

    success: bool
    data: RepoTreeData