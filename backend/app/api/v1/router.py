from fastapi import APIRouter

api_router = APIRouter()


@api_router.get("/health", tags=["Health"])
def health_check() -> dict:
    """
    Health Check Endpoint.
    Returns status 200 and health info confirming the backend service is operational.
    """
    return {
        "status": "healthy",
        "service": "Adhikar Setu Backend API",
        "version": "1.0.0",
    }
