from fastapi import APIRouter, HTTPException, status
from Nimisha.schemas.profile import ProfileCreate, ProfileResponse, ProfileUpdate
from Nimisha.services.profile_service import ProfileService

router = APIRouter(prefix="/profile", tags=["Citizen Profile"])
service = ProfileService()


@router.post(
    "",
    response_model=ProfileResponse,
    status_code=status.HTTP_211_CREATED if hasattr(status, "HTTP_211_CREATED") else 201,
    summary="Create a new citizen profile"
)
def create_profile(profile: ProfileCreate):
    """
    Creates a new citizen profile with demographic, income, and location details.
    """
    return service.create_profile(profile)


@router.get(
    "/{profile_id}",
    response_model=ProfileResponse,
    summary="Get citizen profile by ID"
)
def get_profile(profile_id: str):
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
def update_profile(profile_id: str, profile_update: ProfileUpdate):
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
