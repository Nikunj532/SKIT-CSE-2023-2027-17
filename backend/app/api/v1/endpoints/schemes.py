from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.database.mongodb import get_database
from app.repositories.scheme_repository import SchemeRepository
from app.schemas.scheme import SchemeListResponse, SchemeResponse

router = APIRouter(prefix="/schemes", tags=["Schemes"])


@router.get(
    "/",
    response_model=SchemeListResponse,
    summary="Search & Filter Government Schemes",
)
async def list_schemes(
    q: Optional[str] = Query(None, description="Keyword text search query"),
    state: Optional[str] = Query(None, description="Filter by state (e.g. Puducherry, Rajasthan)"),
    category: Optional[str] = Query(None, description="Filter by scheme category"),
    gender: Optional[str] = Query(None, description="Filter by gender eligibility (male, female, transgender, all)"),
    age: Optional[int] = Query(None, ge=0, le=120, description="Filter by target age"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Results per page"),
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    """
    Search and filter government schemes database with full-text search and structured eligibility filters.
    """
    repo = SchemeRepository(db)
    skip = (page - 1) * limit
    result = await repo.search_schemes(
        query=q,
        state=state,
        category=category,
        gender=gender,
        age=age,
        skip=skip,
        limit=limit,
    )
    return result


@router.get(
    "/stats/summary",
    summary="Get Scheme Database Summary Statistics",
)
async def get_schemes_summary(
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    """Returns database summary metrics including total schemes, unique states, and categories."""
    repo = SchemeRepository(db)
    return await repo.get_summary_stats()


@router.get(
    "/{slug}",
    response_model=SchemeResponse,
    summary="Get Government Scheme Details by Slug",
)
async def get_scheme_by_slug(
    slug: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    """Fetch complete details of a specific government scheme using its unique slug."""
    repo = SchemeRepository(db)
    scheme = await repo.get_by_slug(slug)
    if not scheme:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Government scheme with slug '{slug}' not found.",
        )
    return scheme
