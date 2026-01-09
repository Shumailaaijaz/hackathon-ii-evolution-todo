"""FastAPI application initialization.

This is the main entry point for the Todo API backend.
It configures CORS, lifespan events, and registers API routes.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan context manager for startup and shutdown events.

    This function runs on application startup and shutdown.
    It creates database tables on startup (for development).

    Args:
        app: FastAPI application instance

    Yields:
        None (context manager)

    Note:
        In production, use Alembic migrations instead of create_db_and_tables().
    """
    # Startup: Create database tables (development only)
    if settings.is_development:
        print("🚀 Starting Todo API (Development Mode)")
        print(f"   Database: {settings.DATABASE_URL.split('@')[1].split('?')[0]}")
        print("   Creating database tables...")
        try:
            create_db_and_tables()
            print("   ✓ Database tables ready")
        except Exception as e:
            print(f"   ⚠ Database table creation failed: {e}")
            print("   Continuing anyway (tables may already exist)")
    else:
        print("🚀 Starting Todo API (Production Mode)")

    yield

    # Shutdown
    print("👋 Shutting down Todo API")


# Create FastAPI application
app = FastAPI(
    title="Todo API",
    description="Full-stack todo application API with multi-user authentication",
    version="2.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc",  # ReDoc
    openapi_url="/openapi.json",
    lifespan=lifespan,
    # Additional metadata
    contact={
        "name": "Todo App Support",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,  # Frontend URLs
    allow_credentials=True,  # Allow cookies/auth headers
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
    expose_headers=["*"],  # Expose all headers to frontend
)


# Root endpoint
@app.get(
    "/",
    tags=["Root"],
    summary="API Information",
    response_description="API metadata and available endpoints"
)
async def root() -> dict:
    """Get API information and available endpoints.

    This endpoint provides basic information about the API,
    including version, documentation links, and status.

    Returns:
        Dictionary with API metadata

    Example:
        ```
        GET /
        Response:
        {
            "name": "Todo API",
            "version": "2.0.0",
            "status": "online",
            "documentation": "/docs",
            "environment": "development"
        }
        ```
    """
    return {
        "name": "Todo API",
        "version": "2.0.0",
        "status": "online",
        "documentation": "/docs",
        "redoc": "/redoc",
        "openapi": "/openapi.json",
        "environment": settings.ENVIRONMENT,
        "endpoints": {
            "auth": {
                "signup": "/api/auth/signup",
                "signin": "/api/auth/signin"
            },
            "tasks": "/api/{user_id}/tasks",
            "health": "/health",
        }
    }


# Health check endpoint
@app.get(
    "/health",
    tags=["Health"],
    summary="Health Check",
    response_description="Service health status"
)
async def health_check() -> dict:
    """Check service health and readiness.

    This endpoint is used by load balancers and monitoring systems
    to verify that the service is running and ready to accept requests.

    Returns:
        Dictionary with health status

    Example:
        ```
        GET /health
        Response:
        {
            "status": "healthy",
            "version": "2.0.0",
            "database": "connected"
        }
        ```
    """
    # TODO: Add actual database health check
    return {
        "status": "healthy",
        "version": "2.0.0",
        "environment": settings.ENVIRONMENT,
        "debug": settings.DEBUG,
    }


# Register API routers
from app.api.auth import router as auth_router
from app.api.tasks import router as tasks_router

# Authentication routes
app.include_router(
    auth_router,
    prefix="/api",
    tags=["Authentication"],
    responses={
        400: {"description": "Bad Request - Invalid input"},
        401: {"description": "Unauthorized - Invalid credentials"},
        409: {"description": "Conflict - Resource already exists"},
    }
)

# Task routes (protected)
app.include_router(
    tasks_router,
    prefix="/api",
    tags=["Tasks"],
    responses={
        401: {"description": "Unauthorized - Missing or invalid JWT token"},
        403: {"description": "Forbidden - Access denied to this resource"},
        404: {"description": "Not Found - Resource does not exist"},
    }
)


# Global exception handler for unhandled errors
@app.exception_handler(Exception)
async def global_exception_handler(request, exc: Exception) -> JSONResponse:
    """Handle unhandled exceptions.

    This provides a consistent error response format for unexpected errors.

    Args:
        request: The request that caused the exception
        exc: The exception that was raised

    Returns:
        JSON response with error details
    """
    if settings.DEBUG:
        # In debug mode, include exception details
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "data": None,
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": f"An unexpected error occurred: {str(exc)}",
                    "detail": str(exc) if settings.DEBUG else None
                }
            }
        )
    else:
        # In production, hide exception details
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "data": None,
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "An unexpected error occurred. Please try again later."
                }
            }
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes
        log_level="info" if settings.DEBUG else "warning",
    )
