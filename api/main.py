"""Stars & Pines V2 — FastAPI application entry point."""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from api.db import init_db
from api.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup."""
    try:
        init_db()
        print("Stars & Pines V2 — Database initialized")
    except Exception as e:
        print(f"Stars & Pines V2 — Database init failed: {e}")
        raise
    yield
    print("Stars & Pines V2 — Shutting down")


app = FastAPI(
    title="Stars & Pines V2",
    description="Local-first hospitality operations system",
    version="2.0.0",
    lifespan=lifespan,
)

# CORS — allow all frontend apps to call the API
# NOTE: allow_origins=["*"] with allow_credentials=True is invalid in FastAPI.
# Use explicit origins or drop credentials. Since this is local-first, we use ["*"].
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def mount_if_exists(path: str, directory: str, name: str):
    """Mount a static directory only if it exists, to avoid startup crashes."""
    full_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), directory)
    if os.path.isdir(full_path):
        app.mount(path, StaticFiles(directory=directory, html=True), name=name)
        print(f"  Mounted {path} -> {directory}/")
    else:
        print(f"  WARNING: {directory}/ not found, skipping {path}")


# Mount static files for the frontend apps
mount_if_exists("/guest-entry", "guest-entry", "guest-entry")
mount_if_exists("/guest-portal", "guest-portal", "guest-portal")
mount_if_exists("/family-app", "family-app", "family-app")
mount_if_exists("/shared", "shared", "shared")


@app.middleware("http")
async def add_cache_control(request: Request, call_next):
    """No-cache for HTML pages, cache for static assets."""
    response = await call_next(request)
    path = request.url.path
    if path.endswith(".html") or (path.endswith("/") and not path.startswith("/api")):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    elif path.endswith(".js") or path.endswith(".css"):
        response.headers["Cache-Control"] = "public, max-age=3600"
    return response


# Include API routes
app.include_router(router)


@app.get("/health")
def health_check():
    """Health check — confirms API and database are running."""
    from api.db import get_db
    with get_db() as conn:
        tables = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        ).fetchall()
    return {
        "status": "ok",
        "database": "connected",
        "tables": [row["name"] for row in tables],
    }
