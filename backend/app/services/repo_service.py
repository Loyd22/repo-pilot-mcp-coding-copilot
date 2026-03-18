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