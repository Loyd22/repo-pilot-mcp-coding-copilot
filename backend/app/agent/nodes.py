"""
LangGraph nodes for repository assistant workflow.
"""

from app.agent.state import RepoAgentState
from app.services.git_service import get_git_diff
from app.services.memory_service import get_session_messages
from app.services.repo_service import get_repo_tree, read_repo_file, search_repo
from app.services.llm_service import generate_repo_answer


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

    tool_trace = state.get("tool_trace", [])
    tool_trace.append("load_memory")

    return {
        **state,
        "memory_messages": memory_messages,
        "tool_trace": tool_trace,
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
    elif "what should i build next" in message or "what next" in message:
        intent = "build_next"
    elif "generate implementation prompt" in message or "codex prompt" in message or "cursor prompt" in message:
        intent = "generate_prompt"
    elif "explain this error" in message or "error" in message:
        intent = "explain_error"
    elif "production readiness" in message or "production-ready" in message or "is this production ready" in message:
        intent = "production_review"
    else:
        intent = "unknown"

    tool_trace = state.get("tool_trace", [])
    tool_trace.append(f"classify_request: {intent}")

    return {
        **state,
        "intent": intent,
        "tool_trace": tool_trace,
    }


def run_tool_node(state: RepoAgentState) -> RepoAgentState:
    """Run the appropriate tool based on classified intent."""
    repo_path = state["repo_path"]
    message = state["message"]
    intent = state["intent"]

    files_viewed: list[str] = []
    tool_trace = state.get("tool_trace", [])

    if intent == "repo_tree":
        result = get_repo_tree(repo_path)
        files_viewed = result.get("tree", [])[:20]
        tool_trace.append("run_tool: repo_tree")

    elif intent == "read_file":
        file_path = message[5:].strip()
        result = read_repo_file(repo_path, file_path)
        files_viewed = [result.get("file_path", "")]
        tool_trace.append("run_tool: read_file")

    elif intent == "search":
        query = message[5:].strip()
        result = search_repo(repo_path, query)
        files_viewed = list({match["file_path"] for match in result.get("matches", [])[:20]})
        tool_trace.append("run_tool: search")

    elif intent == "git_diff":
        result = get_git_diff(repo_path)
        files_viewed = result.get("changed_files", [])[:20]
        tool_trace.append("run_tool: git_diff")

    elif intent == "build_next":
        result = {
            "repo_tree": get_repo_tree(repo_path),
            "git_diff": get_git_diff(repo_path),
        }
        files_viewed = result["repo_tree"].get("tree", [])[:20]
        tool_trace.append("run_tool: build_next")

    elif intent == "generate_prompt":
        result = {
            "repo_tree": get_repo_tree(repo_path),
            "git_diff": get_git_diff(repo_path),
        }
        files_viewed = result["repo_tree"].get("tree", [])[:20]
        tool_trace.append("run_tool: generate_prompt")

    elif intent == "production_review":
        result = {
            "repo_tree": get_repo_tree(repo_path),
            "git_diff": get_git_diff(repo_path),
            "config_hits": search_repo(repo_path, "config"),
            "schema_hits": search_repo(repo_path, "schema"),
            "test_hits": search_repo(repo_path, "test"),
            "logging_hits": search_repo(repo_path, "logging"),
        }
        files_viewed = result["repo_tree"].get("tree", [])[:20]
        tool_trace.append("run_tool: production_review")

    elif intent == "explain_error":
        result = {
            "repo_tree": get_repo_tree(repo_path),
            "note": "Use the user message as the main error context.",
        }
        files_viewed = result["repo_tree"].get("tree", [])[:20]
        tool_trace.append("run_tool: explain_error")

    else:
        result = {}
        tool_trace.append("run_tool: unknown")

    return {
        **state,
        "tool_result": result,
        "files_viewed": files_viewed,
        "tool_trace": tool_trace,
    }


def generate_answer_node(state: RepoAgentState) -> RepoAgentState:
    """Generate the final assistant answer using the LLM."""
    answer = generate_repo_answer(
        user_message=state["message"],
        intent=state["intent"],
        repo_path=state["repo_path"],
        memory_messages=state.get("memory_messages", []),
        tool_result=state.get("tool_result", {}),
    )

    tool_trace = state.get("tool_trace", [])
    tool_trace.append("generate_answer: llm")

    return {
        **state,
        "answer": answer,
        "tool_trace": tool_trace,
    }