"""Per-scheme stages: detail (by slug), documents and faqs (by scheme _id).

Each stage is resumable: every record is appended to a JSONL checkpoint, so a
re-run only fetches what is missing. Join key across all files = `slug`.
"""
import json
import logging
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path
from typing import Any, Optional

from . import config
from .fetcher import RateLimitedClient
from .myscheme import _load, load_schemes

log = logging.getLogger(__name__)

STAGES = ("detail", "documents", "faqs")
_OUT = {"detail": config.DETAIL_FILE,
        "documents": config.DOCUMENTS_FILE,
        "faqs": config.FAQS_FILE}


def progress_path(stage: str) -> Path:
    return config.RAW_DIR / f"_{stage}_progress.jsonl"


def failed_path(stage: str) -> Path:
    return config.RAW_DIR / f"schemes_{stage}_failed.json"


def unique_slugs() -> list[str]:
    """Slugs from the saved list, deduped, list order kept (5089 -> 5087)."""
    return list(dict.fromkeys(i["slug"] for i in load_schemes()))


def _read_progress(path: Path) -> dict[str, dict]:
    done: dict[str, dict] = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:  # half-written last line after a crash
                continue
            done[rec["slug"]] = rec
    return done


def _write_json(data: Any, path: Path, pretty: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    kw = {"indent": 2} if pretty else {"separators": (",", ":")}
    tmp.write_text(json.dumps(data, ensure_ascii=False, **kw), encoding="utf-8")
    tmp.replace(path)


def fetch_one(client: RateLimitedClient, stage: str, slug: str,
              scheme_id: Optional[str] = None) -> dict:
    """Fetch one scheme for a stage. Returns {"id", "slug", **data.en}."""
    if stage == "detail":
        payload = client.get_json(config.DETAIL_API_URL,
                                  params={"slug": slug, "lang": "en"})
    else:
        payload = client.get_json(f"{config.DETAIL_API_URL}/{scheme_id}/{stage}",
                                  params={"lang": "en"})
    if payload.get("statusCode") != 200:
        raise RuntimeError(f"Unexpected API response: {str(payload)[:200]}")
    data = payload.get("data")
    if stage == "detail":
        if not data or "en" not in data:
            raise ValueError("no data in response")
        return {"id": data["_id"], "slug": slug, **data["en"]}
    en = (data or {}).get("en") or {}  # scheme may have no docs/faqs -> empty record
    return {"id": scheme_id, "slug": slug, **en}


def fetch_stage(client: RateLimitedClient, stage: str, slugs: list[str],
                limit: Optional[int] = None) -> tuple[int, dict]:
    """Resumable fetch for one stage. Returns (fetched_count, failed_dict)."""
    assert stage in STAGES, stage
    done = _read_progress(progress_path(stage))
    ids: dict[str, str] = {}
    if stage != "detail":  # documents/faqs need scheme _id from the detail stage
        ids = {s: r["id"] for s, r in _read_progress(progress_path("detail")).items()}
    todo = [s for s in slugs if s not in done and (stage == "detail" or s in ids)]
    no_id = sum(1 for s in slugs if s not in done and stage != "detail" and s not in ids)
    if no_id:
        log.warning("%s: %d slugs skipped (detail not fetched yet)", stage, no_id)
    if limit:
        todo = todo[:limit]
    log.info("%s: %d already done, %d to fetch", stage, len(done), len(todo))

    failed: dict[str, str] = {}
    fetched = 0
    progress_path(stage).parent.mkdir(parents=True, exist_ok=True)
    try:
        with progress_path(stage).open("a", encoding="utf-8") as f:
            for n, slug in enumerate(todo, 1):
                try:
                    rec = fetch_one(client, stage, slug, ids.get(slug))
                except Exception as e:  # keep going; failed slugs retried next run
                    failed[slug] = repr(e)
                    log.warning("%s: FAILED %s: %r", stage, slug, e)
                    continue
                f.write(json.dumps(rec, ensure_ascii=False,
                                   separators=(",", ":")) + "\n")
                f.flush()
                fetched += 1
                if n % 100 == 0:
                    log.info("%s: %d / %d", stage, n, len(todo))
    finally:
        _write_json(failed, failed_path(stage), pretty=True)
    return fetched, failed


def build_stage_file(stage: str, slugs: list[str], pretty: bool = False) -> int:
    """Turn the JSONL checkpoint into the final envelope file. Returns item count."""
    done = _read_progress(progress_path(stage))
    items = [done[s] for s in slugs if s in done]
    _write_json({
        "source": config.SOURCE_NAME,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "stage": stage,
        "total": len(slugs),
        "count": len(items),
        "items": items,
    }, _OUT[stage], pretty)
    return len(items)


@lru_cache(maxsize=None)
def _index(stage: str) -> dict[str, dict]:
    return {i["slug"]: i for i in _load(_OUT[stage])["items"]}


def load_scheme_details() -> list[dict]:
    return _load(config.DETAIL_FILE)["items"]


def load_scheme_documents() -> list[dict]:
    return _load(config.DOCUMENTS_FILE)["items"]


def load_scheme_faqs() -> list[dict]:
    return _load(config.FAQS_FILE)["items"]


def get_scheme(slug: str) -> dict:
    """All fetched parts of one scheme, joined by slug (None if a part is missing)."""
    out: dict[str, Any] = {"slug": slug}
    for stage in STAGES:
        try:
            out[stage] = _index(stage).get(slug)
        except FileNotFoundError:
            out[stage] = None
    return out
