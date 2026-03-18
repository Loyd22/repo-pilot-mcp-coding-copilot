"""
Repository-related routes.
"""

from fastapi import APIRouter, HTTPException

from app.schemas.repo import RepoTreeRequest, RepoTreeResponse, RepoTreeData
from app.services.repo_service import get_repo_tree

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