"""
Database models for safe edit proposals.
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base import Base


class EditProposal(Base):
    """Represents a reviewable edit proposal created by the assistant."""

    __tablename__ = "edit_proposals"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id"), nullable=False, index=True)
    repo_path = Column(String, nullable=False)
    user_request = Column(Text, nullable=False)
    title = Column(String, nullable=False)
    summary = Column(Text, nullable=False)
    status = Column(String, nullable=False, default="proposed", index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    session = relationship("ChatSession")
    files = relationship(
        "EditProposalFile",
        back_populates="proposal",
        cascade="all, delete-orphan",
        order_by="EditProposalFile.id.asc()",
    )


class EditProposalFile(Base):
    """Represents a single file change inside an edit proposal."""

    __tablename__ = "edit_proposal_files"

    id = Column(Integer, primary_key=True, index=True)
    proposal_id = Column(Integer, ForeignKey("edit_proposals.id"), nullable=False, index=True)
    file_path = Column(String, nullable=False)
    change_type = Column(String, nullable=False)  # create | update
    before_content = Column(Text, nullable=False, default="")
    after_content = Column(Text, nullable=False)
    diff_text = Column(Text, nullable=False)

    proposal = relationship("EditProposal", back_populates="files")