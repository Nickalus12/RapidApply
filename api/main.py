"""
RapidApply API v2.0
Main FastAPI application entry point
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import time
from typing import Dict, Any

from api.config import settings
from api.middleware.rate_limit import RateLimitMiddleware
from api.middleware.logging import LoggingMiddleware
from api.routers import auth, jobs, applications, users, analytics, resumes
# from api.utils.database import init_db
# from api.utils.redis_client import init_redis

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application startup and shutdown events"""
    # Startup
    logger.info("Starting RapidApply API v2.0...")
    # await init_db()  # Temporarily disabled
    # await init_redis()  # Temporarily disabled
    logger.info("Application startup complete")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")
    # Add cleanup tasks here


# Create FastAPI application
app = FastAPI(
    title="RapidApply API",
    description="AI-Powered LinkedIn Job Application Automation Platform",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS
)

# app.add_middleware(RateLimitMiddleware)  # Temporarily disabled
app.add_middleware(LoggingMiddleware)


# Health check endpoint
@app.get("/health", tags=["health"])
async def health_check() -> Dict[str, Any]:
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "version": "2.0.0",
        "timestamp": time.time()
    }


# Root endpoint
@app.get("/", tags=["root"])
async def root() -> Dict[str, str]:
    """Root endpoint"""
    return {
        "message": "Welcome to RapidApply API v2.0",
        "docs": "/api/docs",
        "health": "/health"
    }


# Exception handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """Handle 404 errors"""
    return JSONResponse(
        status_code=404,
        content={"detail": "Resource not found"}
    )


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    """Handle 500 errors"""
    logger.error(f"Internal error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


# Include routers
app.include_router(
    auth.router,
    prefix="/api/v1/auth",
    tags=["authentication"]
)

app.include_router(
    users.router,
    prefix="/api/v1/users",
    tags=["users"]
)

app.include_router(
    jobs.router,
    prefix="/api/v1/jobs",
    tags=["jobs"]
)

app.include_router(
    applications.router,
    prefix="/api/v1/applications",
    tags=["applications"]
)

app.include_router(
    resumes.router,
    prefix="/api/v1/resumes",
    tags=["resumes"]
)

app.include_router(
    analytics.router,
    prefix="/api/v1/analytics",
    tags=["analytics"]
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )