"""
ADIP — FastAPI Application Entry Point

Registers all API routers under /api/v1 and configures CORS.
Business logic never lives here — only wiring.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config.settings import settings
from backend.utils.logger import get_logger
from backend.api.routes import (
    customers,
    sessions,
    planner,
    knowledge,
    recommendations,
    approvals,
    memory,
    analytics,
)
from backend.memory.database import init_db

logger = get_logger(__name__)

app = FastAPI(
    title="ADIP — Agentic Decision Intelligence Platform",
    description=(
        "Enterprise-grade multi-agent platform for explainable, "
        "evidence-backed Next Best Actions."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS ─────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
PREFIX = settings.api_v1_prefix

app.include_router(customers.router, prefix=PREFIX, tags=["Customers"])
app.include_router(sessions.router, prefix=PREFIX, tags=["Sessions"])
app.include_router(planner.router, prefix=PREFIX, tags=["Planner"])
app.include_router(knowledge.router, prefix=PREFIX, tags=["Knowledge"])
app.include_router(recommendations.router, prefix=PREFIX, tags=["Recommendations"])
app.include_router(approvals.router, prefix=PREFIX, tags=["Approvals"])
app.include_router(memory.router, prefix=PREFIX, tags=["Memory"])
app.include_router(analytics.router, prefix=PREFIX, tags=["Analytics"])


# ── Startup ───────────────────────────────────────────────────────────────────
@app.on_event("startup")
async def startup_event() -> None:
    """Initialize the database on startup."""
    logger.info("ADIP backend starting up...")
    init_db()
    logger.info("Database initialized.")
    logger.info(f"API available at: {PREFIX}")


# ── Health Check ──────────────────────────────────────────────────────────────
@app.get("/health", tags=["Health"])
async def health_check() -> dict:
    """Returns service health status."""
    return {"status": "healthy", "service": "ADIP Backend", "version": "1.0.0"}
