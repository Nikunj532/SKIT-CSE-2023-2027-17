import uuid
from typing import Dict, List, Optional

PROFILES: Dict[str, dict] = {}

SCHEMES: List[dict] = [
    {"id": "edu-001", "name": "National Merit Scholarship", "category": "education",
     "state": "All India", "description": "Scholarship for meritorious students from low-income families."},
    {"id": "agr-001", "name": "PM Kisan Samman Nidhi", "category": "agriculture",
     "state": "All India", "description": "Income support of Rs 6000 per year to farmer families."},
    {"id": "hlt-001", "name": "Ayushman Bharat PM-JAY", "category": "health",
     "state": "All India", "description": "Health cover of Rs 5 lakh per family per year."},
]


def create_profile(data: dict) -> dict:
    pid = uuid.uuid4().hex[:8]
    PROFILES[pid] = {"id": pid, **data}
    return PROFILES[pid]


def update_profile(pid: str, data: dict) -> Optional[dict]:
    if pid not in PROFILES:
        return None
    PROFILES[pid] = {"id": pid, **data}
    return PROFILES[pid]


def get_profile(pid: str) -> Optional[dict]:
    return PROFILES.get(pid)


def list_schemes(q: Optional[str] = None, category: Optional[str] = None) -> List[dict]:
    result = SCHEMES
    if q:
        ql = q.lower()
        result = [s for s in result if ql in s["name"].lower() or ql in s["description"].lower()]
    if category:
        result = [s for s in result if s["category"].lower() == category.lower()]
    return result


def get_scheme(sid: str) -> Optional[dict]:
    for s in SCHEMES:
        if s["id"] == sid:
            return s
    return None
