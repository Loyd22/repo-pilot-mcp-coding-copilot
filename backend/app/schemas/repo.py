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

class RepoFileRequest(BaseModel):
    """Request schema for reading a file from a repository."""

    repo_path: str = Field(..., min_length=1, description="Absolute path to the repository")
    file_path: str = Field(..., min_length=1, description="Relative path to the file inside the repository")

class RepoFileData(BaseModel):
    """Data returned for a file read operation."""

    file_name: str
    file_path: str
    content: str

class RepoFileResponse(BaseModel):
    """Response schema for repository file reading."""

    success: bool
    data: RepoFileData

class RepoSearchRequest(BaseModel):
    """Request schema for searching text inside a repository."""

    repo_path: str = Field(..., min_length=1, description="Absolute path to the repository")
    query: str = Field(..., min_length=1, description="Text to search for inside the repository")

class RepoSearchMatch(BaseModel):
    """Single search match result."""

    file_path: str
    line_number: int
    line_text: str


class RepoSearchData(BaseModel):
    """Data returned for a repository search."""

    query: str
    matches: list[RepoSearchMatch]


class RepoSearchResponse(BaseModel):
    """Response schema for repository search."""

    success: bool
    data: RepoSearchData