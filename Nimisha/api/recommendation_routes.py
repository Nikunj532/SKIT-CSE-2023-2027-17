from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status

from Nimisha.schemas.profile import ProfileBase
from Nimisha.schemas.recommendation import (
    EligibilityCheckResult,
    RecommendationResponse,
)
from Nimisha.services.recommendation_service import RecommendationService

router = APIRouter(tags=["Scheme Recommendations & Eligibility"])

_default_rec_service = RecommendationService()


def get_recommendation_service() -> RecommendationService:
    """Dependency provider for RecommendationService."""
    return _default_rec_service


@router.get(
    "/profile/{profile_id}/recommendations",
    response_model=RecommendationResponse,
    summary="Get Personalized Scheme Recommendations for Citizen Profile",
)
def get_recommendations_for_profile(
    profile_id: str,
    min_score: float = Query(40.0, ge=0.0, le=100.0, description="Minimum eligibility match score threshold"),
    category: Optional[str] = Query(None, description="Filter recommendations by scheme category"),
    limit: int = Query(10, ge=1, le=50, description="Maximum number of recommendations to return"),
    service: RecommendationService = Depends(get_recommendation_service),
):
    """
    Evaluates citizen profile against all government welfare schemes and returns
    personalized, ranked recommendations with transparent eligibility justifications.
    """
    result = service.recommend_by_profile_id(
        profile_id=profile_id,
        min_score=min_score,
        category=category,
        limit=limit,
    )
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Profile with ID '{profile_id}' not found.",
        )
    return result


@router.post(
    "/recommendations",
    response_model=RecommendationResponse,
    summary="Evaluate Personalized Recommendations for Ad-Hoc Citizen Profile",
)
def get_recommendations_for_ad_hoc_profile(
    profile: ProfileBase,
    min_score: float = Query(40.0, ge=0.0, le=100.0, description="Minimum eligibility match score threshold"),
    category: Optional[str] = Query(None, description="Filter recommendations by scheme category"),
    limit: int = Query(10, ge=1, le=50, description="Maximum number of recommendations to return"),
    service: RecommendationService = Depends(get_recommendation_service),
):
    """
    Directly evaluates a citizen demographic and income profile without requiring
    prior database registration. Enables guest and preview eligibility discovery.
    """
    return service.recommend_for_profile(
        profile=profile,
        min_score=min_score,
        category=category,
        limit=limit,
    )


@router.post(
    "/schemes/{scheme_id}/check-eligibility",
    response_model=EligibilityCheckResult,
    summary="Check Citizen Eligibility for Specific Scheme",
)
def check_scheme_eligibility_endpoint(
    scheme_id: str,
    profile: ProfileBase,
    service: RecommendationService = Depends(get_recommendation_service),
):
    """
    Performs an in-depth eligibility audit of a single scheme against a citizen profile,
    returning match score, verified matching criteria, and any missing qualifications.
    """
    result = service.check_scheme_eligibility(profile, scheme_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Scheme with ID '{scheme_id}' not found.",
        )
    return result
