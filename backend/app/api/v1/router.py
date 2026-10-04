from fastapi import APIRouter
from app.database.mongodb import db_manager

api_router = APIRouter()


@api_router.get("/health", tags=["Health"])
async def health_check() -> dict:
    """
    Health Check Endpoint.
    Returns status 200 and health info for backend service and database connection.
    """
    db_status = "connected" if await db_manager.ping() else "disconnected"
    return {
        "status": "healthy" if db_status == "connected" else "degraded",
        "service": "Adhikar Setu Backend API",
        "database": db_status,
        "version": "1.0.0",
    }
