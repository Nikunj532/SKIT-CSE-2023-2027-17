"""
Citizen Schemas: Profile and Recommendation Schemas
"""
from .profile import (
    ProfileBase,
    ProfileCreate,
    ProfileUpdate,
    ProfileResponse,
    ProfileInDB,
    PROFILES_COLLECTION,
    PROFILES_COLLECTION_VALIDATOR,
    PROFILES_INDEXES,
)
from .recommendation import (
    EligibilityStatus,
    SchemeEligibilityMatch,
    RecommendationResponse,
    EligibilityCheckRequest,
    EligibilityCheckResult,
)

__all__ = [
    # Profile
    "ProfileBase",
    "ProfileCreate",
    "ProfileUpdate",
    "ProfileResponse",
    "ProfileInDB",
    "PROFILES_COLLECTION",
    "PROFILES_COLLECTION_VALIDATOR",
    "PROFILES_INDEXES",
    # Recommendation
    "EligibilityStatus",
    "SchemeEligibilityMatch",
    "RecommendationResponse",
    "EligibilityCheckRequest",
    "EligibilityCheckResult",
]
