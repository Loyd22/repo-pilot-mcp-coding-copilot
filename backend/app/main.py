"""
Main FastAPI application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routes.chat import router as chat_router
from app.api.v1.routes.git import router as git_router
from app.api.v1.routes.health import router as health_router
from app.api.v1.routes.memory import router as memory_router
from app.api.v1.routes.repo import router as repo_router
from app.core.config import settings
from app.db.session import engine
from app.models.chat_memory import Base
from app.schemas.common import RootResponse

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.APP_DEBUG,
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=RootResponse, tags=["Root"])
def root() -> RootResponse:
    """Root endpoint."""
    return RootResponse(message="RepoPilot backend is running.")


app.include_router(health_router)
app.include_router(repo_router)
app.include_router(git_router)
app.include_router(chat_router)
app.include_router(memory_router)