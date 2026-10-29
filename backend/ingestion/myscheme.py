"""myScheme.gov.in ingestion: list API fetch, save, and loaders for teammates."""
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from . import config
from .fetcher import RateLimitedClient

log = logging.getLogger(__name__)


def _flatten(hit: dict) -> dict:
    """{'id':..,'fields':{..},'highlight':{}} -> {'id':.., **fields}."""
    return {"id": hit.get("id"), **hit.get("fields", {})}


def _fetch_pass(client: RateLimitedClient, sort: str, page_size: int,
                items: dict[str, dict], limit: Optional[int]) -> Optional[int]:
    """Paginate the list API once for a given sort; merge hits into `items` by id.

    Returns the total reported by the API.
    """
    offset, total = 0, None
    while total is None or offset < total:
        params = {"lang": "en", "q": "[]", "keyword": "", "sort": sort,
                  "from": offset, "size": page_size}
        payload = client.get_json(config.LIST_API_URL, params=params)
        if payload.get("statusCode") != 200:
            raise RuntimeError(f"Unexpected API response: {str(payload)[:200]}")
        hits = payload["data"]["hits"]
        total = hits["page"]["total"]
        batch = hits["items"]
        if not batch:
            break
        for hit in batch:
            items[hit["id"]] = _flatten(hit)
        offset += page_size
        log.info("sort=%r fetched %d / %d unique", sort, len(items), total)
        if limit and len(items) >= limit:
            break
    return total


def fetch_schemes_list(client: RateLimitedClient,
                       page_size: int = config.PAGE_SIZE,
                       limit: Optional[int] = None,
                       sorts: tuple = config.SORTS) -> dict:
    """Fetch all schemes via multi-pass pagination; return the data-contract envelope.

    A single paginated pass can skip/duplicate items, so we run one pass per
    sort order and merge by id until the unique count reaches the API total.
    """
    items: dict[str, dict] = {}
    total = None
    for sort in sorts:
        total = _fetch_pass(client, sort, page_size, items, limit)
        log.info("after pass sort=%r: %d / %s unique", sort, len(items), total)
        if limit and len(items) >= limit:
            break
        if total is not None and len(items) >= total:
            break
    if not limit and total is not None and len(items) < total:
        log.warning("INCOMPLETE: %d of %d (missing %d)",
                    len(items), total, total - len(items))
    out = list(items.values())[:limit] if limit else list(items.values())
    return {
        "source": config.SOURCE_NAME,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "total": total,
        "items": out,
    }


def save_json(data: dict, path: Path) -> None:
    """Atomic JSON write (UTF-8, Hindi-safe)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(path)


def _load(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found. Run: python -m backend.ingestion.run_ingestion")
    return json.loads(path.read_text(encoding="utf-8"))


def load_schemes(with_meta: bool = False):
    """Load saved scheme list (no API hit). Returns items, or full envelope."""
    data = _load(config.LIST_FILE)
    return data if with_meta else data["items"]
