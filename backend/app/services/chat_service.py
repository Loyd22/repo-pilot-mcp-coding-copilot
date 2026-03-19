"""
Simple chat service that routes messages to repository tools.
"""

from app.services.git_service import get_git_diff
from app.services.repo_service import get_repo_tree, read_repo_file, search_repo


def handle_chat_message(repo_path: str, message: str) -> dict:
    """
    Handle a user chat message by selecting the appropriate repository tool.
    """
    normalized_message = message.strip().lower()

    if "explain this repo" in normalized_message or "repo structure" in normalized_message:
        result = get_repo_tree(repo_path)
        tree_preview = "\n".join(result["tree"][:30])

        answer = (
            f"Repository: {result['repo_name']}\n\n"
            f"Here are the first files and folders found:\n{tree_preview}"
        )

        return {
            "intent": "repo_tree",
            "answer": answer,
        }

    if normalized_message.startswith("read "):
        file_path = message[5:].strip()
        result = read_repo_file(repo_path, file_path)

        answer = (
            f"File: {result['file_path']}\n\n"
            f"Content:\n{result['content'][:4000]}"
        )

        return {
            "intent": "read_file",
            "answer": answer,
        }

    if normalized_message.startswith("find "):
        query = message[5:].strip()
        result = search_repo(repo_path, query)

        if not result["matches"]:
            answer = f'No matches found for "{query}".'
        else:
            preview_lines = [
                f'{match["file_path"]} (line {match["line_number"]}): {match["line_text"]}'
                for match in result["matches"][:20]
            ]
            answer = f'Search results for "{query}":\n\n' + "\n".join(preview_lines)

        return {
            "intent": "search",
            "answer": answer,
        }

    if "what changed" in normalized_message or "git diff" in normalized_message or "show changes" in normalized_message:
        result = get_git_diff(repo_path)

        changed_files = result["changed_files"]
        diff_text = result["diff"][:4000]

        if not changed_files:
            answer = "There are no current uncommitted changes in this repository."
        else:
            answer = (
                "Changed files:\n"
                + "\n".join(changed_files)
                + f"\n\nDiff preview:\n{diff_text}"
            )

        return {
            "intent": "git_diff",
            "answer": answer,
        }

    return {
        "intent": "unknown",
        "answer": (
            "I could not understand that request yet.\n\n"
            "Try one of these:\n"
            "- Explain this repo\n"
            "- Read backend/app/main.py\n"
            "- Find FastAPI\n"
            "- What changed?"
        ),
    }