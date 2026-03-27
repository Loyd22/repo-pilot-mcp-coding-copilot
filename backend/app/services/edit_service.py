"""
Service functions for safe edit proposals.
"""

from __future__ import annotations

import difflib
from pathlib import Path

from sqlalchemy.orm import Session

from app.models.chat_memory import ChatSession
from app.models.edit_proposal import EditProposal, EditProposalFile


ALLOWED_CHANGE_TYPES = {"create", "update"}
MAX_FILES_PER_PROPOSAL = 5
BLOCKED_FILE_SUFFIXES = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".pdf",
    ".ico",
    ".exe",
    ".dll",
    ".so",
    ".zip",
    ".tar",
    ".gz",
}


def _resolve_repo_root(repo_path: str) -> Path:
    """Validate and resolve the repository root."""
    root = Path(repo_path).resolve()
    if not root.exists():
        raise FileNotFoundError(f"Repository path does not exist: {repo_path}")
    if not root.is_dir():
        raise NotADirectoryError(f"Repository path is not a directory: {repo_path}")
    return root


def _safe_resolve_file(repo_root: Path, relative_file_path: str) -> Path:
    """Resolve a repo-relative file path and block path traversal."""
    normalized = relative_file_path.replace("\\", "/").strip().lstrip("/")
    candidate = (repo_root / normalized).resolve()

    if repo_root != candidate and repo_root not in candidate.parents:
        raise ValueError(f"Unsafe file path outside repository: {relative_file_path}")

    return candidate


def _is_supported_text_file(file_path: str) -> bool:
    """Return True for normal text/code files."""
    suffix = Path(file_path).suffix.lower()
    return suffix not in BLOCKED_FILE_SUFFIXES


def _make_unified_diff(file_path: str, before_text: str, after_text: str) -> str:
    """Build unified diff text for review."""
    diff = difflib.unified_diff(
        before_text.splitlines(),
        after_text.splitlines(),
        fromfile=f"a/{file_path}",
        tofile=f"b/{file_path}",
        lineterm="",
    )
    return "\n".join(diff)


def create_manual_edit_proposal(
    db: Session,
    session_id: str,
    repo_path: str,
    user_message: str,
    title: str,
    summary: str,
    files: list[dict],
) -> EditProposal:
    """
    Create a safe edit proposal without applying any file changes.

    Expected files format:
    [
        {
            "file_path": "backend/app/example.py",
            "change_type": "update",
            "after_content": "new full file content"
        }
    ]
    """
    repo_root = _resolve_repo_root(repo_path)

    session = db.query(ChatSession).filter(ChatSession.session_id == session_id).first()
    if not session:
        raise ValueError(f"Chat session not found: {session_id}")

    if not files:
        raise ValueError("At least one proposed file change is required.")

    if len(files) > MAX_FILES_PER_PROPOSAL:
        raise ValueError(f"Too many files. Max allowed is {MAX_FILES_PER_PROPOSAL}.")

    proposal = EditProposal(
        session_id=session.id,
        repo_path=repo_path,
        user_request=user_message,
        title=title.strip() or "Proposed repository changes",
        summary=summary.strip() or "Review the proposed changes below.",
        status="proposed",
    )
    db.add(proposal)
    db.flush()

    for item in files:
        file_path = str(item.get("file_path", "")).strip()
        change_type = str(item.get("change_type", "")).strip().lower()
        after_content = str(item.get("after_content", ""))

        if not file_path:
            raise ValueError("Each file change must include file_path.")
        if change_type not in ALLOWED_CHANGE_TYPES:
            raise ValueError(f"Unsupported change type: {change_type}")
        if not _is_supported_text_file(file_path):
            raise ValueError(f"Unsupported file type for safe edit mode: {file_path}")

        target_path = _safe_resolve_file(repo_root, file_path)

        before_content = ""
        if target_path.exists():
            if target_path.is_dir():
                raise IsADirectoryError(f"Expected file but got directory: {file_path}")
            before_content = target_path.read_text(encoding="utf-8")
            if change_type == "create":
                raise ValueError(f"Cannot create an already existing file: {file_path}")
        else:
            if change_type != "create":
                raise FileNotFoundError(
                    f"Cannot update non-existing file. Use create instead: {file_path}"
                )

        diff_text = _make_unified_diff(file_path, before_content, after_content)

        proposal_file = EditProposalFile(
            proposal_id=proposal.id,
            file_path=file_path,
            change_type=change_type,
            before_content=before_content,
            after_content=after_content,
            diff_text=diff_text,
        )
        db.add(proposal_file)

    db.commit()
    db.refresh(proposal)
    return proposal


def get_edit_proposal(db: Session, proposal_id: int) -> EditProposal:
    """Fetch a proposal by ID."""
    proposal = db.query(EditProposal).filter(EditProposal.id == proposal_id).first()
    if not proposal:
        raise FileNotFoundError(f"Edit proposal not found: {proposal_id}")
    return proposal


def approve_edit_proposal(db: Session, proposal_id: int) -> EditProposal:
    """Approve a proposal."""
    proposal = get_edit_proposal(db, proposal_id)

    if proposal.status not in {"proposed", "rejected"}:
        raise ValueError(f"Cannot approve proposal from status: {proposal.status}")

    proposal.status = "approved"
    db.commit()
    db.refresh(proposal)
    return proposal


def reject_edit_proposal(db: Session, proposal_id: int) -> EditProposal:
    """Reject a proposal."""
    proposal = get_edit_proposal(db, proposal_id)

    if proposal.status == "applied":
        raise ValueError("Applied proposals cannot be rejected.")

    proposal.status = "rejected"
    db.commit()
    db.refresh(proposal)
    return proposal


def apply_edit_proposal(db: Session, proposal_id: int) -> EditProposal:
    """Apply an approved proposal to disk."""
    proposal = get_edit_proposal(db, proposal_id)

    if proposal.status != "approved":
        raise ValueError("Only approved proposals can be applied.")

    repo_root = _resolve_repo_root(proposal.repo_path)

    try:
        for proposal_file in proposal.files:
            target_path = _safe_resolve_file(repo_root, proposal_file.file_path)
            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.write_text(proposal_file.after_content, encoding="utf-8")

        proposal.status = "applied"
        db.commit()
        db.refresh(proposal)
        return proposal
    except Exception:
        proposal.status = "failed"
        db.commit()
        db.refresh(proposal)
        raise


def serialize_edit_proposal(proposal: EditProposal) -> dict:
    """Convert EditProposal ORM object to response-safe dict."""
    return {
        "id": proposal.id,
        "session_id": proposal.session.session_id if proposal.session else "",
        "repo_path": proposal.repo_path,
        "user_request": proposal.user_request,
        "title": proposal.title,
        "summary": proposal.summary,
        "status": proposal.status,
        "files": [
            {
                "file_path": file.file_path,
                "change_type": file.change_type,
                "before_content": file.before_content,
                "after_content": file.after_content,
                "diff_text": file.diff_text,
            }
            for file in proposal.files
        ],
    }