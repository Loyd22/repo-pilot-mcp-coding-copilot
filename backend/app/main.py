"""
Main FastAPI application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routes.chat import router as chat_router
from app.api.v1.routes.edit import router as edit_router
from app.api.v1.routes.git import router as git_router
from app.api.v1.routes.health import router as health_router
from app.api.v1.routes.memory import router as memory_router
from app.api.v1.routes.repo import router as repo_router
from app.api.v1.routes.verification import router as verification_router
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine

# Import models before create_all so SQLAlchemy registers them.
from app.models import chat_memory  # noqa: F401
from app.models import edit_proposal  # noqa: F401

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


@app.get("/", tags=["Root"])
def root() -> dict:
    """Root endpoint."""
    return {"message": "RepoPilot backend is running."}


app.include_router(health_router)
app.include_router(repo_router)
app.include_router(git_router)
app.include_router(chat_router)
app.include_router(memory_router)
app.include_router(edit_router)
app.include_router(verification_router)