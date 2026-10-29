import json
import logging
import math
from pathlib import Path
from typing import List, Optional

from backend.schemas.scheme import Scheme, SchemeSearchResponse

logger = logging.getLogger("adhikar_setu.scheme_service")

# Data path locations in priority order
PRIMARY_DATA_PATH = Path("data/processed/schemes.json")
SAMPLE_DATA_PATH = Path("data/sample_schemes.json")


def get_active_data_path(custom_path: Optional[Path] = None) -> Optional[Path]:
    """Resolves which scheme dataset file to load."""
    if custom_path is not None:
        p = Path(custom_path)
        return p if p.exists() else None
    if PRIMARY_DATA_PATH.exists():
        return PRIMARY_DATA_PATH
    if SAMPLE_DATA_PATH.exists():
        return SAMPLE_DATA_PATH
    return None


def load_schemes(data_path: Optional[Path] = None) -> List[Scheme]:
    """
    Loads government schemes from JSON dataset.
    Returns empty list if no dataset file exists.
    """
    resolved_path = get_active_data_path(data_path)
    if resolved_path is None or not resolved_path.exists():
        return []

    try:
        with open(resolved_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        schemes: List[Scheme] = []
        for item in data:
            try:
                schemes.append(Scheme(**item))
            except Exception as e:
                logger.warning("Skipping malformed scheme record: %s", e)
        return schemes
    except (json.JSONDecodeError, OSError) as e:
        logger.error("Failed to load schemes file: %s", e)
        return []


def get_all_schemes(data_path: Optional[Path] = None) -> List[Scheme]:
    """Returns all available schemes without filtering."""
    return load_schemes(data_path=data_path)


def get_scheme_by_id(scheme_id: str, data_path: Optional[Path] = None) -> Optional[Scheme]:
    """
    Retrieves a single scheme by its unique scheme_id.
    """
    schemes = load_schemes(data_path=data_path)
    for scheme in schemes:
        if scheme.scheme_id == scheme_id:
            return scheme
    return None


def search_schemes(
    q: Optional[str] = None,
    category: Optional[str] = None,
    state: Optional[str] = None,
    page: int = 1,
    limit: int = 10,
    data_path: Optional[Path] = None,
) -> SchemeSearchResponse:
    """
    Searches and filters government schemes based on query keywords,
    category, state, and applies pagination.
    """
    schemes = load_schemes(data_path=data_path)

    # 1. Keyword search (q): matches in name, description, ministry, category
    if q and q.strip():
        query_terms = q.strip().lower().split()
        filtered: List[Scheme] = []
        for s in schemes:
            searchable_text = f"{s.name} {s.description} {s.category} {s.ministry or ''}".lower()
            if all(term in searchable_text for term in query_terms):
                filtered.append(s)
        schemes = filtered

    # 2. Category filter
    if category and category.strip():
        cat_lower = category.strip().lower()
        schemes = [
            s for s in schemes
            if s.category and cat_lower in s.category.lower()
        ]

    # 3. State filter (includes state-specific schemes, plus Central / All India)
    if state and state.strip():
        state_lower = state.strip().lower()
        schemes = [
            s for s in schemes
            if s.state and (
                state_lower == s.state.lower()
                or s.state.lower() in ("central", "all", "all india", "national")
            )
        ]

    # 4. Pagination
    total = len(schemes)
    total_pages = math.ceil(total / limit) if total > 0 else 0

    if page < 1:
        page = 1
    if limit < 1:
        limit = 10

    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    page_items = schemes[start_idx:end_idx]

    return SchemeSearchResponse(
        total=total,
        page=page,
        limit=limit,
        total_pages=total_pages,
        schemes=page_items,
    )