"""
State definitions for the LangGraph workflow.
"""

from typing import TypedDict


class RepoAgentState(TypedDict, total=False):
    """State shared across graph nodes."""


    db: any
    session_id: str
    repo_path: str
    message: str
    memory_messages: list[dict]
    intent: str
    tool_result: dict
    answer: str
    tool_trace: list[str]
    files_viewed: list[str]