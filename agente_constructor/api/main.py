"""
Agente_Constructor - Main API Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from config import settings
from shared.db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle management"""
    # Startup
    print("🧬 Initializing Genes Platform...")
    await init_db()
    print("✅ Database initialized")
    yield
    # Shutdown
    print("🔻 Shutting down Genes Platform...")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Autonomous Agent Factory - Dynamic Agent Creation & Management",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """API root"""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "operational",
        "lead_agent": "Agente_Constructor"
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": "2026-05-25T13:28:00Z"
    }


# Import and include routers (will be added next)
# from .routes import agents, tasks
# app.include_router(agents.router, prefix=settings.api_prefix)
# app.include_router(tasks.router, prefix=settings.api_prefix)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )
