"""
This file defines the shared data used by the LangGraph workflow.

Think of this like a shared notebook.
Each step in the workflow can read from it and write to it.
"""

from typing import TypedDict


class RepoAgentState(TypedDict, total=False):
    """
    This is the shared state of the AI workflow.

    Simple meaning:
    - When the workflow starts, it stores information here
    - Each node updates this state
    - The next node reads what the previous node added
    """

    # Database connection/session
    db: object

    # Unique chat session ID
    session_id: str

    # Path of the repository the user wants to analyze
    repo_path: str

    # The user's message from the chat UI
    message: str

    # Previous messages from memory, so the AI remembers context
    memory_messages: list[dict]

    # The detected meaning of the user's request
    # Example: repo_tree, search, git_diff, propose_edit
    intent: str

    # The raw result returned by the tool/service
    tool_result: dict

    # Final answer shown to the user
    answer: str

    # Step-by-step trace of what the workflow did
    tool_trace: list[str]

    # Files that were viewed or involved in the request
    files_viewed: list[str]

    # If Phase 8 creates an edit proposal, store its ID here
    edit_proposal_id: int | None

    # Status of the edit proposal
    # Example: proposed, approved, applied
    edit_proposal_status: str | None

    # Short summary of the proposal
    edit_summary: str | None

     # New Phase 9 fields
    verification_summary: str | None
    verification_results: list[dict] | None