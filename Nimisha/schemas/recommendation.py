from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

from backend.schemas.scheme import Scheme
from Nimisha.schemas.profile import ProfileBase


class EligibilityStatus(str, Enum):
    ELIGIBLE = "Eligible"
    CONDITIONALLY_ELIGIBLE = "Conditionally Eligible"
    INELIGIBLE = "Ineligible"


class SchemeEligibilityMatch(BaseModel):
    """
    Detailed eligibility evaluation and recommendation for a single government scheme.
    """
    scheme_id: str = Field(..., description="Unique scheme identifier")
    name: str = Field(..., description="Name of the government scheme")
    category: str = Field(..., description="Scheme category (e.g. Agriculture, Education, Health)")
    state: Optional[str] = Field(None, description="Applicable state or Central")
    ministry: Optional[str] = Field(None, description="Nodal ministry or department")
    official_url: Optional[str] = Field(None, description="Official portal link")
    
    is_eligible: bool = Field(..., description="Whether the citizen meets the core criteria")
    match_score: float = Field(..., ge=0.0, le=100.0, description="Match confidence score from 0.0 to 100.0")
    eligibility_status: EligibilityStatus = Field(..., description="Eligibility determination status")
    matched_criteria: List[str] = Field(default_factory=list, description="List of criteria successfully met")
    missing_criteria: List[str] = Field(default_factory=list, description="List of unmet criteria or requirements")
    recommendation_reason: str = Field(..., description="Concise citizen-friendly justification")
    benefits_summary: List[str] = Field(default_factory=list, description="Key scheme benefits")


class RecommendationResponse(BaseModel):
    """
    Personalized scheme recommendations response tailored to a citizen's profile.
    """
    profile_id: Optional[str] = Field(None, description="Profile ID if evaluated for an existing profile")
    citizen_name: Optional[str] = Field(None, description="Citizen name")
    state: Optional[str] = Field(None, description="Citizen state")
    category: Optional[str] = Field(None, description="Citizen social category")
    occupation: Optional[str] = Field(None, description="Citizen occupation")
    total_recommended: int = Field(..., description="Count of recommended schemes")
    total_evaluated: int = Field(..., description="Total schemes evaluated in dataset")
    recommendations: List[SchemeEligibilityMatch] = Field(
        default_factory=list,
        description="Ranked list of recommended schemes ordered by match score"
    )


class EligibilityCheckRequest(BaseModel):
    """
    Request model for evaluating scheme eligibility against an ad-hoc profile.
    """
    profile: ProfileBase = Field(..., description="Citizen demographic and socio-economic profile")
    scheme_id: Optional[str] = Field(None, description="Optional specific scheme_id to check against")


class EligibilityCheckResult(BaseModel):
    """
    Detailed audit response for a single scheme eligibility check.
    """
    scheme_id: str = Field(..., description="Target scheme identifier")
    scheme_name: str = Field(..., description="Scheme title")
    is_eligible: bool = Field(..., description="Whether citizen is eligible")
    eligibility_status: EligibilityStatus = Field(..., description="Eligibility status")
    match_score: float = Field(..., description="Score out of 100")
    matched_criteria: List[str] = Field(..., description="Verified matching criteria")
    missing_criteria: List[str] = Field(..., description="Criteria requiring further documentation or not met")
    recommendation_reason: str = Field(..., description="Summary reason")
