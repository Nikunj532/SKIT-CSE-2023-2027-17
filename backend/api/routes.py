from fastapi import APIRouter

from backend.services.scheme_service import get_all_schemes


router = APIRouter()


@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Adhikar Setu"
    }


@router.get("/schemes")
def get_schemes():
    return get_all_schemes()