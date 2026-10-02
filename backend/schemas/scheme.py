from pydantic import BaseModel
from typing import List, Optional


class Scheme(BaseModel):
    scheme_id: str
    name: str
    description: str
    ministry: Optional[str] = None
    state: Optional[str] = None
    category: str
    benefits: List[str] = []
    eligibility: List[str] = []
    documents: List[str] = []
    application_process: List[str] = []
    official_url: Optional[str] = None
