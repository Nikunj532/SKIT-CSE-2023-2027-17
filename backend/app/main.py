from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.router import api_router

app = FastAPI(
    title=settings.APP_NAME,
    description="Backend API for Adhikar Setu - Multilingual AI Assistant for Government Scheme Discovery",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register v1 router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/", tags=["Root"])
def read_root() -> dict:
    """
    Root Endpoint.
    Returns a simple welcoming message and service status.
    """
    return {
        "message": "Welcome to Adhikar Setu Backend API",
        "status": "running",
        "docs": "/docs",
    }
