"""
This file runs safe verification commands for the repository.

Simple meaning:
- After code changes, we can run checks like build, lint, and syntax validation
- Each check is run as a shell command
- The results are collected and returned in a structured way
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


# These are the verification checks we allow for now.
# Each check has:
# - a command to run
# - a working folder inside the repo
#
# Important for Windows:
# - use "npm.cmd" instead of "npm"
# - use sys.executable instead of plain "python"
ALLOWED_CHECKS = {
    "frontend_build": {
        "command": ["npm.cmd", "run", "build"],
        "cwd": "frontend",
    },
    "frontend_lint": {
        "command": ["npm.cmd", "run", "lint"],
        "cwd": "frontend",
    },
    "frontend_typecheck": {
        "command": ["npm.cmd", "run", "type-check"],
        "cwd": "frontend",
    },
    "backend_syntax": {
        "command": [sys.executable, "-m", "compileall", "app"],
        "cwd": "backend",
    },
}


# These are the default checks that run when the user says
# things like "verify this repo"
DEFAULT_CHECKS = [
    "frontend_build",
    "frontend_lint",
    "backend_syntax",
]


def _resolve_repo_root(repo_path: str) -> Path:
    """
    Validate and resolve the repository root path.

    Simple meaning:
    - Make sure the repo path exists
    - Make sure it is a folder
    """
    root = Path(repo_path).resolve()

    if not root.exists():
        raise FileNotFoundError(f"Repository path does not exist: {repo_path}")

    if not root.is_dir():
        raise NotADirectoryError(f"Repository path is not a directory: {repo_path}")

    return root


def _run_command(command: list[str], working_directory: Path) -> dict:
    """
    Run one verification command and capture the result.

    Simple meaning:
    - Execute the command
    - Save exit code, stdout, and stderr
    - Return a structured result
    """
    completed = subprocess.run(
        command,
        cwd=str(working_directory),
        capture_output=True,
        text=True,
        shell=False,
    )

    return {
        "success": completed.returncode == 0,
        "exit_code": completed.returncode,
        "stdout": completed.stdout.strip(),
        "stderr": completed.stderr.strip(),
    }


def run_verification(repo_path: str, checks: list[str] | None = None) -> dict:
    """
    Run one or more verification checks for the repository.

    Simple meaning:
    - Use default checks if none are provided
    - Only allow known safe checks
    - Return all results together
    """
    repo_root = _resolve_repo_root(repo_path)

    selected_checks = checks or DEFAULT_CHECKS
    results: list[dict] = []

    for check_name in selected_checks:
        if check_name not in ALLOWED_CHECKS:
            raise ValueError(f"Unsupported verification check: {check_name}")

        check_config = ALLOWED_CHECKS[check_name]
        working_directory = (repo_root / check_config["cwd"]).resolve()

        if not working_directory.exists():
            results.append(
                {
                    "name": check_name,
                    "success": False,
                    "exit_code": 1,
                    "stdout": "",
                    "stderr": f"Working directory does not exist: {working_directory}",
                }
            )
            continue

        command_result = _run_command(check_config["command"], working_directory)

        results.append(
            {
                "name": check_name,
                "success": command_result["success"],
                "exit_code": command_result["exit_code"],
                "stdout": command_result["stdout"],
                "stderr": command_result["stderr"],
            }
        )

    overall_success = all(result["success"] for result in results) if results else False

    return {
        "repo_path": repo_path,
        "overall_success": overall_success,
        "results": results,
    }