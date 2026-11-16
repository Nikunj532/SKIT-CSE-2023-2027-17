from typing import Optional
from fastapi import APIRouter, HTTPException
from backend.app.repositories import sprint2_store as store

router = APIRouter(prefix="/api/v2/schemes", tags=["Schemes (Sprint 2)"])


@router.get("")
def search_schemes(q: Optional[str] = None, category: Optional[str] = None):
    items = store.list_schemes(q, category)
    return {"count": len(items), "results": items}


@router.get("/{scheme_id}")
def scheme_detail(scheme_id: str):
    s = store.get_scheme(scheme_id)
    if not s:
        raise HTTPException(status_code=404, detail="Scheme not found")
    return s
