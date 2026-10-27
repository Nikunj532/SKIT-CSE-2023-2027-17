from pydantic import BaseModel, Field
from typing import List, Optional


class Scheme(BaseModel):
    scheme_id: str = Field(..., description="Unique scheme identifier")
    name: str = Field(..., description="Name of the government scheme")
    description: str = Field(..., description="Brief summary of the scheme")
    ministry: Optional[str] = Field(None, description="Nodal ministry or department")
    state: Optional[str] = Field(None, description="Applicable state or 'Central' / 'All'")
    category: str = Field(..., description="Scheme category (e.g. Agriculture, Education, Health)")
    benefits: List[str] = Field(default_factory=list, description="Key benefits provided by the scheme")
    eligibility: List[str] = Field(default_factory=list, description="Eligibility criteria")
    documents: List[str] = Field(default_factory=list, description="Required documents")
    application_process: List[str] = Field(default_factory=list, description="Step-by-step application instructions")
    official_url: Optional[str] = Field(None, description="Official portal or source URL")


class SchemeSearchResponse(BaseModel):
    """Paginated response model for scheme search and filtering."""
    total: int = Field(..., description="Total count of schemes matching query and filters")
    page: int = Field(..., description="Current page number (1-indexed)")
    limit: int = Field(..., description="Maximum results per page")
    total_pages: int = Field(..., description="Total number of available pages")
    schemes: List[Scheme] = Field(default_factory=list, description="List of matching scheme objects")
