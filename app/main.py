import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.api.v1.router import api_router


def create_application() -> FastAPI:
    """
    Application factory function.

    Why a function instead of just writing app = FastAPI() at the top?
    Because this lets you create different versions of the app:
    - create_application() for production
    - a test version with different settings for pytest

    Everything that configures the app happens inside this function.
    """

    # Rate limiter — limits requests per IP address
    # key_func=get_remote_address means we identify users by IP
    limiter = Limiter(key_func=get_remote_address)

    # Create the FastAPI application
    application = FastAPI(
        title=settings.APP_NAME,
        # Where the auto-generated OpenAPI schema lives
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        # Where the interactive Swagger UI lives
        docs_url=f"{settings.API_V1_STR}/docs",
        # Where the ReDoc documentation lives
        redoc_url=f"{settings.API_V1_STR}/redoc",
        debug=settings.DEBUG,
    )

    # Attach the rate limiter to the app
    # The limiter reads app.state.limiter in every endpoint
    application.state.limiter = limiter

    # Tell FastAPI how to handle rate limit errors
    application.add_exception_handler(
        RateLimitExceeded,
        _rate_limit_exceeded_handler
    )

    # SlowAPI middleware intercepts every request to check rate limits
    application.add_middleware(SlowAPIMiddleware)

    # CORS middleware — allows browsers from other domains to call your API
    # In production, replace allow_origins=["*"] with your actual frontend URL
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Create the uploads folder if it does not exist
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    os.makedirs(f"{settings.UPLOAD_DIR}/restaurants", exist_ok=True)
    os.makedirs(f"{settings.UPLOAD_DIR}/foods", exist_ok=True)

    # Serve uploaded files at /uploads/...
    # e.g. an image saved at uploads/restaurants/abc.jpg
    # is accessible at http://localhost:8000/uploads/restaurants/abc.jpg
    application.mount(
        "/uploads",
        StaticFiles(directory=settings.UPLOAD_DIR),
        name="uploads",
    )

    # Connect all your API routes
    # Every route will be prefixed with /api/v1
    # e.g. auth routes become /api/v1/auth/login
    application.include_router(
        api_router,
        prefix=settings.API_V1_STR
    )

    # Register your custom exception handlers
    register_exception_handlers(application)

    return application


# Create the app instance
# uvicorn imports this object: uvicorn app.main:app
app = create_application()


# A simple health check endpoint
# Always useful to confirm the app is running
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Returns a simple response to confirm the app is alive.
    Used by Docker, load balancers, and monitoring tools.
    """
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": "1.0.0",
    }