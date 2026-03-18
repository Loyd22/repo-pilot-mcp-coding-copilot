"""
Repository-related routes.
"""

from fastapi import APIRouter, HTTPException

from app.schemas.repo import RepoTreeRequest, RepoTreeResponse, RepoTreeData
from app.services.repo_service import get_repo_tree, read_repo_file, search_repo
from app.schemas.repo import (
    RepoTreeRequest,
    RepoTreeResponse,
    RepoTreeData,
    RepoFileRequest,
    RepoFileResponse,
    RepoFileData,
    RepoSearchRequest,
    RepoSearchResponse,
    RepoSearchData,
)

router = APIRouter(prefix="/api/v1/repo", tags=["Repository"])


@router.post("/tree", response_model=RepoTreeResponse)
def scan_repo_tree(payload: RepoTreeRequest) -> RepoTreeResponse:
    """Scan a repository and return its folder/file tree."""
    try:
        result = get_repo_tree(payload.repo_path)
        return RepoTreeResponse(
            success=True,
            data=RepoTreeData(**result),
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except NotADirectoryError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(exc)}") from exc
    

@router.post("/file", response_model=RepoFileResponse)
def get_repo_file(payload: RepoFileRequest) -> RepoFileResponse:
    """Read a file inside a repository and return its contents."""
    try:
        result = read_repo_file(payload.repo_path, payload.file_path)
        return RepoFileResponse(
            success=True,
            data=RepoFileData(**result),
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except NotADirectoryError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except IsADirectoryError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(exc)}") from exc
    

@router.post("/search", response_model=RepoSearchResponse)
def search_repo_text(payload: RepoSearchRequest) -> RepoSearchResponse:
    """Search for text across repository files."""
    try:
        result = search_repo(payload.repo_path, payload.query)
        return RepoSearchResponse(
            success=True,
            data=RepoSearchData(**result),
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except NotADirectoryError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(exc)}") from exc