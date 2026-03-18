"""
Services for repository inspection.
"""

from pathlib import Path


def get_repo_tree(repo_path: str) -> dict:
    """
    Scan a repository path and return a flat list of relative file and folder paths.
    """
    root = Path(repo_path)

    if not root.exists():
        raise FileNotFoundError("Repository path does not exist.")

    if not root.is_dir():
        raise NotADirectoryError("Provided path is not a directory.")

    tree: list[str] = []

    for path in sorted(root.rglob("*")):
        relative_path = path.relative_to(root).as_posix()

        # Skip common unnecessary folders
        if any(part in {".git", "node_modules", "venv", "__pycache__", ".pytest_cache", "dist", "build"} for part in path.parts):
            continue

        if path.is_dir():
            tree.append(f"{relative_path}/")
        else:
            tree.append(relative_path)

    return {
        "repo_name": root.name,
        "tree": tree,
    }

def read_repo_file(repo_path: str, file_path: str) -> dict:
    """
    Read a file inside the repository and return its contents.
    """
    root = Path(repo_path)

    if not root.exists():
        raise FileNotFoundError("Repository path does not exist.")

    if not root.is_dir():
        raise NotADirectoryError("Provided repository path is not a directory.")

    target_file = (root / file_path).resolve()

    if not target_file.exists():
        raise FileNotFoundError("File does not exist inside the repository.")

    if not target_file.is_file():
        raise IsADirectoryError("Provided file path is a directory, not a file.")

    # Prevent path traversal outside the repo
    if root.resolve() not in target_file.parents and target_file != root.resolve():
        raise PermissionError("Access to files outside the repository is not allowed.")

    # Skip common unwanted folders
    blocked_parts = {".git", "node_modules", "venv", "__pycache__", ".pytest_cache", "dist", "build"}
    if any(part in blocked_parts for part in target_file.parts):
        raise PermissionError("Access to this file is not allowed.")

    try:
        content = target_file.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("File is not a readable UTF-8 text file.") from exc

    return {
        "file_name": target_file.name,
        "file_path": file_path.replace("\\", "/"),
        "content": content,
    }

def search_repo(repo_path: str, query: str) -> dict:
    """
    Search for a text query across repository text files.
    """
    root = Path(repo_path)

    if not root.exists():
        raise FileNotFoundError("Repository path does not exist.")

    if not root.is_dir():
        raise NotADirectoryError("Provided repository path is not a directory.")

    blocked_parts = {".git", "node_modules", "venv", "__pycache__", ".pytest_cache", "dist", "build"}
    matches: list[dict] = []

    for file_path in sorted(root.rglob("*")):
        if not file_path.is_file():
            continue

        if any(part in blocked_parts for part in file_path.parts):
            continue

        try:
            lines = file_path.read_text(encoding="utf-8").splitlines()
        except (UnicodeDecodeError, OSError):
            continue

        for index, line in enumerate(lines, start=1):
            if query.lower() in line.lower():
                matches.append(
                    {
                        "file_path": file_path.relative_to(root).as_posix(),
                        "line_number": index,
                        "line_text": line.strip(),
                    }
                )

    return {
        "query": query,
        "matches": matches,
    }