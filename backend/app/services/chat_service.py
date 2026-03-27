"""
This file runs the main chat workflow.

Simple meaning:
- The chat route calls this service
- This service runs the LangGraph workflow
- Then it returns the result back to the route
"""

from sqlalchemy.orm import Session

from app.agent.graph import build_repo_agent

# Build the workflow one time and reuse it
repo_agent = build_repo_agent()


def handle_chat_message(db: Session, session_id: str, repo_path: str, message: str) -> dict:
    """
    Run the full AI workflow for one chat message.

    Input:
    - database session
    - chat session id
    - repository path
    - user message

    Output:
    - intent
    - answer
    - tool trace
    - files viewed
    - edit proposal metadata if Phase 8 was triggered
    """
    result = repo_agent.invoke(
        {
            "db": db,
            "session_id": session_id,
            "repo_path": repo_path,
            "message": message,
            "tool_trace": [],
            "files_viewed": [],
            "edit_proposal_id": None,
            "edit_proposal_status": None,
            "edit_summary": None,
            "verification_summary": None,
            "verification_results": None,
        }
    )

    return {
        "intent": result.get("intent", "unknown"),
        "answer": result.get("answer", "No answer generated."),
        "tool_trace": result.get("tool_trace", []),
        "files_viewed": result.get("files_viewed", []),
        "edit_proposal_id": result.get("edit_proposal_id"),
        "edit_proposal_status": result.get("edit_proposal_status"),
        "edit_summary": result.get("edit_summary"),
        "verification_summary": result.get("verification_summary"),
        "verification_results": result.get("verification_results"),
    }