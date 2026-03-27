"""
This file contains the main steps (nodes) of the AI workflow.

Simple meaning:
1. Load memory
2. Understand the user's request
3. Run the correct tool
4. Generate the final answer
"""

from app.agent.state import RepoAgentState
from app.services.edit_service import create_manual_edit_proposal
from app.services.git_service import get_git_diff
from app.services.llm_service import generate_repo_answer
from app.services.memory_service import get_session_messages
from app.services.repo_service import get_repo_tree, read_repo_file, search_repo
from app.services.verification_service import DEFAULT_CHECKS, run_verification


def load_memory_node(state: RepoAgentState) -> RepoAgentState:
    """Load earlier messages from memory."""
    db = state["db"]
    session_id = state["session_id"]

    messages = get_session_messages(db, session_id)
    memory_messages = [{"role": message.role, "content": message.content} for message in messages]

    tool_trace = state.get("tool_trace", [])
    tool_trace.append("load_memory")

    return {
        **state,
        "memory_messages": memory_messages,
        "tool_trace": tool_trace,
    }


def classify_request_node(state: RepoAgentState) -> RepoAgentState:
    """Decide what kind of request the user made."""
    message = state["message"].strip().lower()

    if (
        "fix " in message
        or "change " in message
        or "update " in message
        or "edit " in message
        or "modify " in message
        or "patch " in message
        or "refactor " in message
        or "implement " in message
        or "create file" in message
        or "create a file" in message
        or "create a new file" in message
        or "add route" in message
        or "add endpoint" in message
    ):
        intent = "propose_edit"

    elif (
        "verify" in message
        or "run build" in message
        or "run lint" in message
        or "type check" in message
        or "type-check" in message
        or "check if this works" in message
        or "check build" in message
    ):
        intent = "verify_repo"

    elif "explain this repo" in message or "repo structure" in message:
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
    """Run the correct tool or service based on intent."""
    db = state["db"]
    repo_path = state["repo_path"]
    message = state["message"]
    intent = state["intent"]

    files_viewed: list[str] = []
    tool_trace = state.get("tool_trace", [])

    edit_proposal_id = None
    edit_proposal_status = None
    edit_summary = None

    verification_summary = None
    verification_results = None

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

    elif intent == "propose_edit":
        sample_files = [
            {
                "file_path": "backend/test_phase8_output.py",
                "change_type": "create",
                "after_content": "print('phase 8 test works from chat')\n",
            }
        ]

        proposal = create_manual_edit_proposal(
            db=db,
            session_id=state["session_id"],
            repo_path=repo_path,
            user_message=message,
            title="Chat-generated safe edit proposal",
            summary="This proposal was created from the chat workflow for Phase 8 testing.",
            files=sample_files,
        )

        result = {
            "proposal_id": proposal.id,
            "title": proposal.title,
            "summary": proposal.summary,
            "status": proposal.status,
            "files": [
                {
                    "file_path": file.file_path,
                    "change_type": file.change_type,
                    "diff_text": file.diff_text,
                }
                for file in proposal.files
            ],
        }

        files_viewed = [file.file_path for file in proposal.files]
        edit_proposal_id = proposal.id
        edit_proposal_status = proposal.status
        edit_summary = proposal.summary
        tool_trace.append("run_tool: propose_edit")

    elif intent == "verify_repo":
        result = run_verification(repo_path=repo_path, checks=DEFAULT_CHECKS)
        verification_results = result["results"]

        passed_count = sum(1 for item in verification_results if item["success"])
        total_count = len(verification_results)

        verification_summary = (
            f"Verification finished. Passed {passed_count} out of {total_count} checks."
        )

        tool_trace.append("run_tool: verify_repo")

    else:
        result = {}
        tool_trace.append("run_tool: unknown")

    return {
        **state,
        "tool_result": result,
        "files_viewed": files_viewed,
        "tool_trace": tool_trace,
        "edit_proposal_id": edit_proposal_id,
        "edit_proposal_status": edit_proposal_status,
        "edit_summary": edit_summary,
        "verification_summary": verification_summary,
        "verification_results": verification_results,
    }


def generate_answer_node(state: RepoAgentState) -> RepoAgentState:
    """Create the final assistant answer."""
    if state.get("intent") == "propose_edit" and state.get("edit_proposal_id"):
        proposal_id = state["edit_proposal_id"]
        status = state.get("edit_proposal_status", "proposed")
        summary = state.get("edit_summary", "")

        answer = (
            f"I created a safe edit proposal.\n\n"
            f"Proposal ID: {proposal_id}\n"
            f"Status: {status}\n"
            f"Summary: {summary}\n\n"
            f"This is review-only for now. Approve it first, then apply it."
        )

    elif state.get("intent") == "verify_repo" and state.get("verification_results") is not None:
        results = state["verification_results"]
        summary = state.get("verification_summary", "Verification finished.")

        lines = [summary, ""]

        for item in results:
            status_text = "PASSED" if item["success"] else "FAILED"
            lines.append(f"- {item['name']}: {status_text}")

            if item["stderr"]:
                lines.append(f"  Error: {item['stderr'][:300]}")

        answer = "\n".join(lines)

    else:
        answer = generate_repo_answer(
            user_message=state["message"],
            intent=state["intent"],
            repo_path=state["repo_path"],
            memory_messages=state.get("memory_messages", []),
            tool_result=state.get("tool_result", {}),
        )

    tool_trace = state.get("tool_trace", [])
    tool_trace.append("generate_answer")

    return {
        **state,
        "answer": answer,
        "tool_trace": tool_trace,
    }