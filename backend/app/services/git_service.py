"""
Services for git-related repository inspection.
"""

from pathlib import Path
import subprocess


def get_git_diff(repo_path: str) -> dict:
    """
    Return changed files and git diff for a repository.
    """
    root = Path(repo_path)

    if not root.exists():
        raise FileNotFoundError("Repository path does not exist.")

    if not root.is_dir():
        raise NotADirectoryError("Provided repository path is not a directory.")

    git_dir = root / ".git"
    if not git_dir.exists():
        raise FileNotFoundError("Provided path is not a Git repository.")

    try:
        status_result = subprocess.run(
            ["git", "status", "--short"],
            cwd=root,
            capture_output=True,
            text=True,
            check=True,
        )

        diff_result = subprocess.run(
            ["git", "diff"],
            cwd=root,
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(f"Git command failed: {exc.stderr.strip() or exc.stdout.strip()}") from exc
    except FileNotFoundError as exc:
        raise RuntimeError("Git is not installed or not available in PATH.") from exc

    changed_files: list[str] = []

    for line in status_result.stdout.splitlines():
        if not line.strip():
            continue

        parts = line.split(maxsplit=1)
        if len(parts) == 2:
            changed_files.append(parts[1].strip().replace("\\", "/"))

    return {
        "changed_files": changed_files,
        "diff": diff_result.stdout,
    }