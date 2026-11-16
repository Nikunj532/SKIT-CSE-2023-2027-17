from typing import Optional, List
from pydantic import BaseModel


class ProfileIn(BaseModel):
    name: str
    age: Optional[int] = None
    gender: Optional[str] = None
    state: Optional[str] = None
    category: Optional[str] = None
    annual_income: Optional[int] = None
    education: Optional[str] = None
    interests: Optional[List[str]] = None
