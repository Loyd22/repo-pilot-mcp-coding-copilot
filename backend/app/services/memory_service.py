"""
Services for chat memory and session persistence.
"""

from sqlalchemy.orm import Session

from app.models.chat_memory import ChatMessage, ChatSession


def get_or_create_session(db: Session, session_id: str, repo_path: str) -> ChatSession:
    """Get an existing session or create a new one."""
    session = db.query(ChatSession).filter(ChatSession.session_id == session_id).first()

    if session:
        if session.repo_path != repo_path:
            session.repo_path = repo_path
            db.commit()
            db.refresh(session)
        return session

    session = ChatSession(session_id=session_id, repo_path=repo_path)
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def save_message(db: Session, session_db_id: int, role: str, content: str) -> ChatMessage:
    """Save a message in a session."""
    message = ChatMessage(session_id=session_db_id, role=role, content=content)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def get_session_messages(db: Session, session_id: str) -> list[ChatMessage]:
    """Get all messages for a session."""
    session = db.query(ChatSession).filter(ChatSession.session_id == session_id).first()

    if not session:
        return []

    return (
        db.query(ChatMessage)
        .filter(ChatMessage.session_id == session.id)
        .order_by(ChatMessage.created_at.asc(), ChatMessage.id.asc())
        .all()
    )