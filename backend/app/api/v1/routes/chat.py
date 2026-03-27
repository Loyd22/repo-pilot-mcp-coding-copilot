"""
This file defines the /api/v1/chat endpoint.

Simple meaning:
- The frontend sends a message here
- This route handles the request
- It saves memory
- It runs the AI workflow
- It saves the assistant reply
- Then it returns the result to the frontend
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
    """
    Main chat endpoint.

    Flow:
    1. Create or get the session
    2. Save the user's message into memory
    3. Run the chat workflow
    4. Save the assistant reply into memory
    5. Return the final response
    """
    try:
        # Make sure the session exists
        session = get_or_create_session(db, payload.session_id, payload.repo_path)

        # Save the user's message first
        save_message(db, session.id, "user", payload.message)

        # Run the AI workflow
        result = handle_chat_message(
            db=db,
            session_id=payload.session_id,
            repo_path=payload.repo_path,
            message=payload.message,
        )

        # Save the assistant reply into memory too
        save_message(db, session.id, "assistant", result["answer"])

        # Return structured response back to the frontend
        return ChatResponse(
            success=True,
            session_id=payload.session_id,
            user_message=payload.message,
            intent=result["intent"],
            answer=result["answer"],
            tool_trace=result["tool_trace"],
            files_viewed=result["files_viewed"],
            edit_proposal_id=result.get("edit_proposal_id"),
            edit_proposal_status=result.get("edit_proposal_status"),
            edit_summary=result.get("edit_summary"),
            verification_summary=result.get("verification_summary"),
            verification_results=result.get("verification_results"),
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
        # Catch any unexpected error
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(exc)}") from exc