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


class ProfileInDB(ProfileBase):
    """
    MongoDB Entity representation for citizen profiles stored in MongoDB.
    Includes the MongoDB internal _id (ObjectId string) alongside the business profile_id.
    """
    id: Optional[str] = Field(None, alias="_id", description="MongoDB ObjectId string")
    profile_id: str = Field(..., description="Unique business profile identifier (e.g. prof_12345678)")
    created_at: str = Field(..., description="Creation timestamp in ISO format")
    updated_at: str = Field(..., description="Last update timestamp in ISO format")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "670678e5f1a23b4c5d6e7f80",
                "profile_id": "prof_a1b2c3d4",
                "name": "Nimisha Mangal",
                "age": 21,
                "gender": "Female",
                "state": "Rajasthan",
                "district": "Jaipur",
                "income": 250000.0,
                "occupation": "Student",
                "category": "General",
                "disability_status": "No",
                "qualification": "B.Tech Data Science",
                "created_at": "2026-10-09T18:00:00Z",
                "updated_at": "2026-10-09T18:00:00Z"
            }
        }


# MongoDB collection name
PROFILES_COLLECTION = "profiles"

# MongoDB JSON Schema validator for the 'profiles' collection
PROFILES_COLLECTION_VALIDATOR = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": [
            "profile_id",
            "name",
            "age",
            "gender",
            "state",
            "district",
            "income",
            "occupation",
            "category",
            "created_at",
            "updated_at"
        ],
        "properties": {
            "profile_id": {"bsonType": "string", "description": "Unique business profile identifier"},
            "name": {"bsonType": "string", "minLength": 2, "maxLength": 100},
            "age": {"bsonType": "int", "minimum": 0, "maximum": 120},
            "gender": {"bsonType": "string"},
            "state": {"bsonType": "string", "minLength": 2},
            "district": {"bsonType": "string", "minLength": 2},
            "income": {"bsonType": ["double", "int"], "minimum": 0},
            "occupation": {"bsonType": "string", "minLength": 2},
            "category": {"bsonType": "string"},
            "disability_status": {"bsonType": "string"},
            "qualification": {"bsonType": ["string", "null"]},
            "created_at": {"bsonType": "string"},
            "updated_at": {"bsonType": "string"}
        }
    }
}

# MongoDB indexes for collection performance & constraints
PROFILES_INDEXES = [
    {"keys": [("profile_id", 1)], "unique": True, "name": "idx_profile_id_unique"},
    {"keys": [("state", 1)], "name": "idx_profile_state"},
    {"keys": [("category", 1)], "name": "idx_profile_category"},
    {"keys": [("created_at", -1)], "name": "idx_profile_created_at"}
]
