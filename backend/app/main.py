from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.router import api_router
from app.database.mongodb import db_manager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("adhikar_setu")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle event handler for managing MongoDB connection startup and shutdown."""
    logger.info("Starting up Adhikar Setu Backend...")
    try:
        await db_manager.connect()
    except Exception as e:
        logger.warning("Could not connect to MongoDB on startup: %s", e)
    yield
    logger.info("Shutting down Adhikar Setu Backend...")
    await db_manager.close()


app = FastAPI(
    title=settings.APP_NAME,
    description="Backend API for Adhikar Setu - Multilingual AI Assistant for Government Scheme Discovery",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
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
