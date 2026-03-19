"""
Chat service powered by LangGraph workflow.
"""

from sqlalchemy.orm import Session

from app.agent.graph import build_repo_agent

repo_agent = build_repo_agent()


def handle_chat_message(db: Session, session_id: str, repo_path: str, message: str) -> dict:
    """
    Run the LangGraph-powered repository assistant workflow.
    """
    result = repo_agent.invoke(
        {
            "db": db,
            "session_id": session_id,
            "repo_path": repo_path,
            "message": message,
            "tool_trace": [],
            "files_viewed": [],
        }
    )

    return {
        "intent": result.get("intent", "unknown"),
        "answer": result.get("answer", "No answer generated."),
        "tool_trace": result.get("tool_trace", []),
        "files_viewed": result.get("files_viewed", []),
    }