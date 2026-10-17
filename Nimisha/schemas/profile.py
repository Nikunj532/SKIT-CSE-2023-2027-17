from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ProfileBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Full name of the citizen")
    age: int = Field(..., ge=0, le=120, description="Age in years")
    gender: str = Field(..., description="Gender (e.g. Male, Female, Transgender, Other)")
    state: str = Field(..., min_length=2, description="State of residence")
    district: str = Field(..., min_length=2, description="District of residence")
    income: float = Field(..., ge=0, description="Annual household income in INR")
    occupation: str = Field(..., min_length=2, description="Occupation / employment type")
    category: str = Field(..., description="Social category (e.g. General, OBC, SC, ST, EWS)")
    disability_status: str = Field(default="No", description="Disability status (Yes/No)")
    qualification: Optional[str] = Field(default=None, description="Highest educational qualification")


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    age: Optional[int] = Field(default=None, ge=0, le=120)
    gender: Optional[str] = None
    state: Optional[str] = Field(default=None, min_length=2)
    district: Optional[str] = Field(default=None, min_length=2)
    income: Optional[float] = Field(default=None, ge=0)
    occupation: Optional[str] = Field(default=None, min_length=2)
    category: Optional[str] = None
    disability_status: Optional[str] = None
    qualification: Optional[str] = None


class ProfileResponse(ProfileBase):
    profile_id: str = Field(..., description="Unique profile identifier")
    created_at: str = Field(..., description="Creation timestamp in ISO format")
    updated_at: str = Field(..., description="Last update timestamp in ISO format")
