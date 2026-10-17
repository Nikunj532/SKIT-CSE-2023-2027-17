from fastapi import APIRouter

from backend.services.scheme_service import get_all_schemes
from Nimisha.api.profile_routes import router as profile_router

router = APIRouter()
router.include_router(profile_router)


@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Adhikar Setu"
    }


@router.get("/schemes")
def get_schemes():
    return get_all_schemes()