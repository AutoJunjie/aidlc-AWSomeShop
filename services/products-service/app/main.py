"""Main FastAPI application."""
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import init_db
from app.routes import products, internal, health
from app.middleware.auth import AuthenticationError, AuthorizationError
import logging
import sys

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format='{"time": "%(asctime)s", "level": "%(levelname)s", "module": "%(name)s", "message": "%(message)s"}',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(products.router)
app.include_router(internal.router)


# Exception handlers
@app.exception_handler(AuthenticationError)
async def authentication_error_handler(request: Request, exc: AuthenticationError):
    """Handle authentication errors."""
    logger.warning(f"Authentication error: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": "UNAUTHORIZED", "detail": exc.detail}
    )


@app.exception_handler(AuthorizationError)
async def authorization_error_handler(request: Request, exc: AuthorizationError):
    """Handle authorization errors."""
    logger.warning(f"Authorization error: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": "FORBIDDEN", "detail": exc.detail}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "INTERNAL_SERVER_ERROR", "detail": "An unexpected error occurred"}
    )


@app.on_event("startup")
async def startup_event():
    """Startup event - initialize database."""
    logger.info(f"Starting {settings.app_name}...")
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        # Don't exit, let health check handle it


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event."""
    logger.info(f"Shutting down {settings.app_name}...")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": settings.app_name,
        "version": "1.0.0",
        "status": "running"
    }
