from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status

from Nimisha.schemas.profile import ProfileCreate, ProfileResponse, ProfileUpdate
from Nimisha.services.profile_service import ProfileService

router = APIRouter(prefix="/profile", tags=["Citizen Profile"])

# Default singleton service instance
_default_profile_service = ProfileService()


def get_profile_service() -> ProfileService:
    """FastAPI dependency provider for ProfileService."""
    return _default_profile_service


@router.post(
    "",
    response_model=ProfileResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new citizen profile"
)
def create_profile(
    profile: ProfileCreate,
    service: ProfileService = Depends(get_profile_service)
):
    """
    Creates a new citizen profile with demographic, income, and location details.
    """
    try:
        return service.create_profile(profile)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create profile: {str(e)}"
        )


@router.get(
    "/{profile_id}",
    response_model=ProfileResponse,
    summary="Get citizen profile by ID"
)
def get_profile(
    profile_id: str,
    service: ProfileService = Depends(get_profile_service)
):
    """
    Retrieves an existing citizen profile by its unique profile ID.
    """
    profile = service.get_profile(profile_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Profile with ID '{profile_id}' not found."
        )
    return profile


@router.put(
    "/{profile_id}",
    response_model=ProfileResponse,
    summary="Update an existing citizen profile"
)
def update_profile(
    profile_id: str,
    profile_update: ProfileUpdate,
    service: ProfileService = Depends(get_profile_service)
):
    """
    Updates specific attributes of an existing citizen profile.
    """
    updated_profile = service.update_profile(profile_id, profile_update)
    if not updated_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Profile with ID '{profile_id}' not found."
        )
    return updated_profile


@router.get(
    "",
    response_model=List[ProfileResponse],
    summary="List citizen profiles"
)
def list_profiles(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of records to return"),
    service: ProfileService = Depends(get_profile_service)
):
    """
    Lists citizen profiles with optional pagination.
    """
    return service.list_profiles(skip=skip, limit=limit)
