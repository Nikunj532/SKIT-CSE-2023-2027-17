from fastapi import APIRouter, HTTPException
from backend.app.schemas.profile import ProfileIn
from backend.app.repositories import sprint2_store as store

router = APIRouter(prefix="/api/v2/profile", tags=["Profile (Sprint 2)"])


def _to_dict(p: ProfileIn) -> dict:
    return p.model_dump() if hasattr(p, "model_dump") else p.dict()


@router.post("", status_code=201)
def create_profile(profile: ProfileIn):
    return store.create_profile(_to_dict(profile))


@router.put("/{profile_id}")
def update_profile(profile_id: str, profile: ProfileIn):
    updated = store.update_profile(profile_id, _to_dict(profile))
    if not updated:
        raise HTTPException(status_code=404, detail="Profile not found")
    return updated


@router.get("/{profile_id}")
def get_profile(profile_id: str):
    p = store.get_profile(profile_id)
    if not p:
        raise HTTPException(status_code=404, detail="Profile not found")
    return p
