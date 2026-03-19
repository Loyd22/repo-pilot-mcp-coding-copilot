"""
LangGraph nodes for repository assistant workflow.
"""

from app.services.git_service import get_git_diff
from app.services.memory_service import get_session_messages
from app.services.repo_service import get_repo_tree, read_repo_file, search_repo
from app.agent.state import RepoAgentState


def load_memory_node(state: RepoAgentState) -> RepoAgentState:
    """Load memory messages for the current session."""
    db = state["db"]
    session_id = state["session_id"]

    messages = get_session_messages(db, session_id)

    memory_messages = [
        {
            "role": message.role,
            "content": message.content,
        }
        for message in messages
    ]

    return {
        **state,
        "memory_messages": memory_messages,
    }


def classify_request_node(state: RepoAgentState) -> RepoAgentState:
    """Classify the user request into a supported intent."""
    message = state["message"].strip().lower()

    if "explain this repo" in message or "repo structure" in message:
        intent = "repo_tree"
    elif message.startswith("read "):
        intent = "read_file"
    elif message.startswith("find "):
        intent = "search"
    elif "what changed" in message or "git diff" in message or "show changes" in message:
        intent = "git_diff"
    else:
        intent = "unknown"

    return {
        **state,
        "intent": intent,
    }


def run_tool_node(state: RepoAgentState) -> RepoAgentState:
    """Run the appropriate tool based on classified intent."""
    repo_path = state["repo_path"]
    message = state["message"]
    intent = state["intent"]

    if intent == "repo_tree":
        result = get_repo_tree(repo_path)
    elif intent == "read_file":
        file_path = message[5:].strip()
        result = read_repo_file(repo_path, file_path)
    elif intent == "search":
        query = message[5:].strip()
        result = search_repo(repo_path, query)
    elif intent == "git_diff":
        result = get_git_diff(repo_path)
    else:
        result = {}

    return {
        **state,
        "tool_result": result,
    }


def generate_answer_node(state: RepoAgentState) -> RepoAgentState:
    """Generate the final assistant answer from tool output."""
    intent = state["intent"]
    result = state.get("tool_result", {})

    if intent == "repo_tree":
        tree_preview = "\n".join(result.get("tree", [])[:30])
        answer = (
            f"Repository: {result.get('repo_name', 'Unknown')}\n\n"
            f"Here are the first files and folders found:\n{tree_preview}"
        )
    elif intent == "read_file":
        answer = (
            f"File: {result.get('file_path', '')}\n\n"
            f"Content:\n{result.get('content', '')[:4000]}"
        )
    elif intent == "search":
        matches = result.get("matches", [])
        query = result.get("query", "")

        if not matches:
            answer = f'No matches found for "{query}".'
        else:
            preview_lines = [
                f'{match["file_path"]} (line {match["line_number"]}): {match["line_text"]}'
                for match in matches[:20]
            ]
            answer = f'Search results for "{query}":\n\n' + "\n".join(preview_lines)
    elif intent == "git_diff":
        changed_files = result.get("changed_files", [])
        diff_text = result.get("diff", "")[:4000]

        if not changed_files:
            answer = "There are no current uncommitted changes in this repository."
        else:
            answer = (
                "Changed files:\n"
                + "\n".join(changed_files)
                + f"\n\nDiff preview:\n{diff_text}"
            )
    else:
        answer = (
            "I could not understand that request yet.\n\n"
            "Try one of these:\n"
            "- Explain this repo\n"
            "- Read backend/app/main.py\n"
            "- Find FastAPI\n"
            "- What changed?"
        )

    return {
        **state,
        "answer": answer,
    }