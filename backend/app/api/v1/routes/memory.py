"""
Memory routes for session history.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.memory_service import get_session_messages

router = APIRouter(prefix="/api/v1/memory", tags=["Memory"])


@router.get("/history/{session_id}")
def get_history(session_id: str, db: Session = Depends(get_db)):
    """Get chat history for a session."""
    messages = get_session_messages(db, session_id)

    return {
        "success": True,
        "session_id": session_id,
        "messages": [
            {
                "role": message.role,
                "content": message.content,
                "created_at": message.created_at,
            }
            for message in messages
        ],
    }