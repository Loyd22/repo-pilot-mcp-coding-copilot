"""
Routes for safe edit proposal workflow.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.edit import (
    EditActionResponse,
    EditProposalData,
    EditProposalRequest,
    EditProposalResponse,
)
from app.services.edit_service import (
    apply_edit_proposal,
    approve_edit_proposal,
    create_manual_edit_proposal,
    get_edit_proposal,
    reject_edit_proposal,
    serialize_edit_proposal,
)

router = APIRouter(prefix="/api/v1/edit", tags=["Edit"])


@router.post("/propose", response_model=EditProposalResponse)
def propose_edit(payload: EditProposalRequest, db: Session = Depends(get_db)) -> EditProposalResponse:
    """
    Create a reviewable edit proposal.

    For now, this route creates a sample placeholder proposal.
    In the next step, we will connect this to the AI/LangGraph flow.
    """
    try:
        sample_files = [
            {
                "file_path": "backend/app/schemas/chat.py",
                "change_type": "update",
                "after_content": "# TODO: replace with AI-generated content\n",
            }
        ]

        proposal = create_manual_edit_proposal(
            db=db,
            session_id=payload.session_id,
            repo_path=payload.repo_path,
            user_message=payload.message,
            title="Sample safe edit proposal",
            summary="This is the first working proposal route for Phase 8.",
            files=sample_files,
        )

        return EditProposalResponse(
            success=True,
            data=EditProposalData(**serialize_edit_proposal(proposal)),
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except (ValueError, NotADirectoryError, IsADirectoryError, PermissionError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(exc)}") from exc


@router.get("/{proposal_id}", response_model=EditProposalResponse)
def get_edit(proposal_id: int, db: Session = Depends(get_db)) -> EditProposalResponse:
    """Fetch a full edit proposal."""
    try:
        proposal = get_edit_proposal(db, proposal_id)
        return EditProposalResponse(
            success=True,
            data=EditProposalData(**serialize_edit_proposal(proposal)),
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(exc)}") from exc


@router.post("/{proposal_id}/approve", response_model=EditActionResponse)
def approve_edit(proposal_id: int, db: Session = Depends(get_db)) -> EditActionResponse:
    """Approve an edit proposal."""
    try:
        proposal = approve_edit_proposal(db, proposal_id)
        return EditActionResponse(
            success=True,
            proposal_id=proposal.id,
            status=proposal.status,
            message="Edit proposal approved.",
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(exc)}") from exc


@router.post("/{proposal_id}/reject", response_model=EditActionResponse)
def reject_edit(proposal_id: int, db: Session = Depends(get_db)) -> EditActionResponse:
    """Reject an edit proposal."""
    try:
        proposal = reject_edit_proposal(db, proposal_id)
        return EditActionResponse(
            success=True,
            proposal_id=proposal.id,
            status=proposal.status,
            message="Edit proposal rejected.",
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(exc)}") from exc


@router.post("/{proposal_id}/apply", response_model=EditActionResponse)
def apply_edit(proposal_id: int, db: Session = Depends(get_db)) -> EditActionResponse:
    """Apply an approved edit proposal."""
    try:
        proposal = apply_edit_proposal(db, proposal_id)
        return EditActionResponse(
            success=True,
            proposal_id=proposal.id,
            status=proposal.status,
            message="Edit proposal applied successfully.",
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(exc)}") from exc