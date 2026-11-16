"""
Citizen Authentication API routes for Adhikar Setu.
Provides Email ID & Password registration, login, and profile token verification.
"""

from datetime import datetime, timezone
import hashlib
import re
import secrets
from typing import Dict, Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field, field_validator

router = APIRouter(prefix="/auth", tags=["Citizen Authentication"])

# Simple in-memory user registry with pre-seeded demo accounts
# Can be synced with MongoDB collection when database is active
_USER_DB: Dict[str, dict] = {
    "ramesh.farmer@example.com": {
        "user_id": "usr_farmer_01",
        "name": "Ramesh Kumar",
        "email": "ramesh.farmer@example.com",
        "password_hash": hashlib.sha256("password123".encode()).hexdigest(),
        "created_at": "2026-10-01T10:00:00Z"
    },
    "pooja.sharma@example.com": {
        "user_id": "usr_student_02",
        "name": "Pooja Sharma",
        "email": "pooja.sharma@example.com",
        "password_hash": hashlib.sha256("password123".encode()).hexdigest(),
        "created_at": "2026-10-01T10:00:00Z"
    },
    "sunita.devi@example.com": {
        "user_id": "usr_rural_03",
        "name": "Sunita Devi",
        "email": "sunita.devi@example.com",
        "password_hash": hashlib.sha256("password123".encode()).hexdigest(),
        "created_at": "2026-10-01T10:00:00Z"
    }
}


def _hash_password(password: str) -> str:
    """Hashes a password with SHA-256 for secure comparison."""
    return hashlib.sha256(password.strip().encode()).hexdigest()


class UserRegisterRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Full name of the citizen")
    email: str = Field(..., description="Valid email address")
    password: str = Field(..., min_length=6, description="Password (at least 6 characters)")

    @field_validator("email")
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        clean = v.strip().lower()
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(pattern, clean):
            raise ValueError("Invalid email format. Please provide a valid email address.")
        return clean


class UserLoginRequest(BaseModel):
    email: str = Field(..., description="Registered email address")
    password: str = Field(..., description="Account password")

    @field_validator("email")
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        clean = v.strip().lower()
        if "@" not in clean or "." not in clean:
            raise ValueError("Invalid email format.")
        return clean


class UserInfo(BaseModel):
    user_id: str
    name: str
    email: str
    created_at: str


class AuthResponse(BaseModel):
    status: str = "success"
    message: str
    access_token: str
    token_type: str = "bearer"
    user: UserInfo


@router.post(
    "/register",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new citizen account using Email & Password"
)
def register_user(req: UserRegisterRequest):
    """
    Registers a new citizen with their full name, email address, and secure password.
    """
    email = req.email
    if email in _USER_DB:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email address already exists. Please sign in."
        )

    user_id = f"usr_{secrets.token_hex(4)}"
    now = datetime.now(timezone.utc).isoformat()
    record = {
        "user_id": user_id,
        "name": req.name.strip(),
        "email": email,
        "password_hash": _hash_password(req.password),
        "created_at": now
    }
    _USER_DB[email] = record

    token = f"jwt_sim_{secrets.token_hex(16)}"
    return AuthResponse(
        message="Account created successfully",
        access_token=token,
        user=UserInfo(
            user_id=user_id,
            name=record["name"],
            email=record["email"],
            created_at=record["created_at"]
        )
    )


@router.post(
    "/login",
    response_model=AuthResponse,
    summary="Citizen login using Email ID & Password"
)
def login_user(req: UserLoginRequest):
    """
    Authenticates a citizen using their email and password.
    Returns an access token and citizen user profile info.
    """
    email = req.email
    password_hash = _hash_password(req.password)

    user_data = _USER_DB.get(email)
    if not user_data or user_data["password_hash"] != password_hash:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password. Please verify your credentials."
        )

    token = f"jwt_sim_{secrets.token_hex(16)}"
    return AuthResponse(
        message="Login successful",
        access_token=token,
        user=UserInfo(
            user_id=user_data["user_id"],
            name=user_data["name"],
            email=user_data["email"],
            created_at=user_data["created_at"]
        )
    )


@router.get(
    "/demo-accounts",
    summary="Get list of demo accounts for evaluation and quick testing"
)
def get_demo_accounts():
    """Returns sample demo accounts with pre-configured credentials for presentation."""
    return [
        {
            "name": u["name"],
            "email": u["email"],
            "default_password": "password123"
        }
        for u in _USER_DB.values()
    ]

