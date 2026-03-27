"""
This file defines the request and response shapes for verification endpoints.

Simple meaning:
- VerificationRequest = what the frontend sends
- VerificationResponse = what the backend sends back
"""

from pydantic import BaseModel, Field

class VerificationRequest(BaseModel):
    """Request body for running repo verification."""

    # Chat session ID, useful for future tracking/logging
    session_id: str = Field(..., min_length=1, description="Chat session ID")

    # Absolute path to the repository to verify
    repo_path: str = Field(..., min_length=1, description="Absolute path to the repository")

    # Optional list of checks to run
    # Example: ["frontend_build", "frontend_lint"]
    checks: list[str] | None = None

class VerificationCheckResult(BaseModel):
    """One check result inside the verification response."""

    # Name of the check
    name: str

    # Whether the check passed
    success: bool

    # Exit code from the command
    exit_code: int

    # Standard output from the command
    stdout: str

    # Standard error from the command
    stderr: str

class VerificationData(BaseModel):
    """Full verification result payload."""

    repo_path: str
    overall_success: bool
    results: list[VerificationCheckResult]

class VerificationResponse(BaseModel):
    """Response body returned by verification endpoints."""

    success: bool
    data: VerificationData