"""
This file defines verification endpoints.

Simple meaning:
- The frontend or Swagger can call these endpoints
- The backend runs verification checks
- Then it returns the results
"""

from fastapi import APIRouter, HTTPException

from app.schemas.verification import (
    VerificationCheckResult,
    VerificationData,
    VerificationRequest,
    VerificationResponse,
)
from app.services.verification_service import run_verification

router = APIRouter(prefix="/api/v1/verify", tags=["Verification"])


@router.post("", response_model=VerificationResponse)
def verify_repo(payload: VerificationRequest) -> VerificationResponse:
    """
    Run verification checks for the given repository.
    """
    try:
        verification_result = run_verification(
            repo_path=payload.repo_path,
            checks=payload.checks,
        )

        return VerificationResponse(
            success=True,
            data=VerificationData(
                repo_path=verification_result["repo_path"],
                overall_success=verification_result["overall_success"],
                results=[
                    VerificationCheckResult(**result)
                    for result in verification_result["results"]
                ],
            ),
        )

    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    except NotADirectoryError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected verification error: {str(exc)}",
        ) from exc