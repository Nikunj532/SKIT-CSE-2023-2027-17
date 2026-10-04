from typing import Optional, List, Any
from pydantic import BaseModel, Field


class SchemeBase(BaseModel):
    """Base Pydantic model for Government Scheme."""

    slug: str = Field(..., description="Unique scheme slug identifier")
    name: str = Field(..., description="Official scheme name")
    description: Optional[str] = Field(None, description="Detailed scheme description")
    ministry: Optional[str] = Field(None, description="Associated ministry")
    department: Optional[str] = Field(None, description="Associated department")
    state: Optional[str] = Field(None, description="Target state or All India")
    category: Optional[str] = Field(None, description="Scheme category tags")
    beneficiary_type: Optional[str] = Field(None, description="Target beneficiaries")
    benefits: Optional[str] = Field(None, description="Detailed benefits description")
    eligibility_text: Optional[str] = Field(None, description="Textual eligibility criteria")
    application_process: Optional[str] = Field(None, description="Steps to apply")
    documents_required: Optional[str] = Field(None, description="List of required documents")
    apply_url: Optional[str] = Field(None, description="Application link")
    official_url: Optional[str] = Field(None, description="Official portal URL")

    # Structured Eligibility Parameters
    eligibility_age_min: Optional[float] = Field(None, description="Minimum age requirement")
    eligibility_age_max: Optional[float] = Field(None, description="Maximum age requirement")
    eligibility_gender: Optional[str] = Field("all", description="Eligible gender (male, female, all)")
    eligibility_caste: Optional[List[str]] = Field(default_factory=list, description="Eligible caste categories")
    eligibility_income_max: Optional[float] = Field(None, description="Maximum annual income ceiling")
    eligibility_residence: Optional[str] = Field(None, description="Residence type (rural, urban, both)")
    eligibility_state: Optional[List[str]] = Field(default_factory=list, description="Eligible states list")
    eligibility_disability: Optional[bool] = Field(False, description="Disability specific scheme")
    eligibility_bpl: Optional[bool] = Field(False, description="BPL (Below Poverty Line) requirement")


class SchemeCreate(SchemeBase):
    """Schema for creating a new scheme."""

    pass


class SchemeResponse(SchemeBase):
    """Schema for returning scheme response."""

    id: Optional[str] = Field(None, alias="_id", description="MongoDB ObjectId string")

    class Config:
        populate_by_name = True


class SchemeListResponse(BaseModel):
    """Paginated list response for schemes."""

    total: int = Field(..., description="Total count matching filters")
    page: int = Field(..., description="Current page number")
    limit: int = Field(..., description="Number of items per page")
    schemes: List[SchemeResponse] = Field(..., description="List of scheme objects")
