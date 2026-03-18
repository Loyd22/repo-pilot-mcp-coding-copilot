"""
Git-related routes.
"""

from fastapi import APIRouter, HTTPException

from app.schemas.git import GitDiffRequest, GitDiffResponse, GitDiffData
from app.services.git_service import get_git_diff

router = APIRouter(prefix="/api/v1/git", tags=["Git"])


@router.post("/diff", response_model=GitDiffResponse)
def read_git_diff(payload: GitDiffRequest) -> GitDiffResponse:
    """Return current git diff for a repository."""
    try:
        result = get_git_diff(payload.repo_path)
        return GitDiffResponse(
            success=True,
            data=GitDiffData(**result),
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except NotADirectoryError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(exc)}") from exc