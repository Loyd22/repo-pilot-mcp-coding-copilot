"""
Common response schemas for the API.
"""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Response schema for health check endpoint."""

    status: str
    app_name: str
    environment: str


class RootResponse(BaseModel):
    """Response schema for root endpoint."""

    message: str