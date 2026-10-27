from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, status

from backend.schemas.scheme import Scheme, SchemeSearchResponse
from backend.services.scheme_service import (
    get_all_schemes,
    get_scheme_by_id,
    search_schemes,
)
from Nimisha.api.profile_routes import router as profile_router

router = APIRouter()

# Register citizen profile routes
router.include_router(profile_router)


@router.get(
    "/health",
    tags=["Health"],
    summary="API Health Check"
)
def health_check():
    """Returns application health status and service identification."""
    return {
        "status": "healthy",
        "service": "Adhikar Setu"
    }


@router.get(
    "/schemes/search",
    response_model=SchemeSearchResponse,
    tags=["Schemes"],
    summary="Search & Filter Government Schemes"
)
def search_schemes_endpoint(
    q: Optional[str] = Query(None, description="Keyword text search query matching name, description, or ministry"),
    category: Optional[str] = Query(None, description="Filter by scheme category (e.g. Agriculture, Education, Health)"),
    state: Optional[str] = Query(None, description="Filter by state name (e.g. Rajasthan) or Central"),
    page: int = Query(1, ge=1, description="Page number for pagination"),
    limit: int = Query(10, ge=1, le=100, description="Results per page (1 to 100)"),
):
    """
    Search and filter government schemes with keyword text search, category filtering,
    state/central filtering, and paginated results.
    """
    return search_schemes(q=q, category=category, state=state, page=page, limit=limit)


@router.get(
    "/schemes/{scheme_id}",
    response_model=Scheme,
    tags=["Schemes"],
    summary="Get Scheme Details by Scheme ID"
)
def get_scheme_by_id_endpoint(scheme_id: str):
    """
    Retrieves full details of a government scheme by its unique scheme_id.
    """
    scheme = get_scheme_by_id(scheme_id)
    if not scheme:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Scheme with ID '{scheme_id}' not found."
        )
    return scheme


@router.get(
    "/schemes",
    response_model=List[Scheme],
    tags=["Schemes"],
    summary="Get All Government Schemes"
)
def get_schemes():
    """
    Returns the list of all available government schemes.
    Preserved for backward compatibility.
    """
    return get_all_schemes()