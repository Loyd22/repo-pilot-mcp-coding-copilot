"""
Chat routes.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import handle_chat_message
from app.services.memory_service import get_or_create_session, save_message

router = APIRouter(prefix="/api/v1", tags=["Chat"])


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest, db: Session = Depends(get_db)) -> ChatResponse:
    """Handle a simple chat request for repository assistance with session memory."""
    try:
        session = get_or_create_session(db, payload.session_id, payload.repo_path)

        save_message(db, session.id, "user", payload.message)

        result = handle_chat_message(
        db=db,
        session_id=payload.session_id,
        repo_path=payload.repo_path,
        message=payload.message,
)

        save_message(db, session.id, "assistant", result["answer"])

        return ChatResponse(
            success=True,
            session_id=payload.session_id,
            user_message=payload.message,
            intent=result["intent"],
            answer=result["answer"],
            tool_trace=result["tool_trace"],
            files_viewed=result["files_viewed"],
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
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(exc)}") from exc