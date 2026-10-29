"""Central config for ingestion. Paths are relative to repo root (no hardcoding)."""
from pathlib import Path

PROJECT_ROOT: Path = Path(__file__).resolve().parents[2]
RAW_DIR: Path = PROJECT_ROOT / "data" / "raw" / "myscheme"
LIST_FILE: Path = RAW_DIR / "schemes_list.json"
DETAIL_FILE: Path = RAW_DIR / "schemes_detail.json"

SOURCE_NAME: str = "myscheme.gov.in"
LIST_API_URL: str = "https://www.myscheme.gov.in/api/apisetu/search/schemes"

PAGE_SIZE: int = 100
REQUEST_DELAY_SEC: float = 1.0
TIMEOUT_SEC: int = 30
MAX_RETRIES: int = 5

HEADERS: dict = {
    "User-Agent": "AdhikarSetu-Academic-Project/1.0 (SKIT Jaipur)",
    "Accept": "application/json",
}

# Sort passes tried in order; results merged by id until total is reached.
# Needed because a single paginated pass can skip/duplicate items.
SORTS: tuple = ("schemename-asc", "schemename-desc", "")

DETAIL_API_URL: str = "https://www.myscheme.gov.in/api/apisetu/schemes"
DOCUMENTS_FILE: Path = RAW_DIR / "schemes_documents.json"
FAQS_FILE: Path = RAW_DIR / "schemes_faqs.json"
