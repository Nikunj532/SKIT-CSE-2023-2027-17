"""Sprint 2: clean and merge myScheme list/detail/documents/faqs (+ HF CSV) into one flat dataset.

Output: data/processed/myscheme/schemes_clean.json  ({source, built_at, total, items})
Run:    python -m backend.cleaning.run_cleaning
Load:   from backend.cleaning import load_clean_schemes
"""
import html
import json
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "myscheme"
HF_CSV = ROOT / "data" / "raw" / "Schemes.csv"
OUT = ROOT / "data" / "processed" / "myscheme" / "schemes_clean.json"

# our field -> HF CSV column; used only when our field is empty
HF_TEXT = {
    "description": "description",
    "benefits": "benefits",
    "eligibility": "eligibility_text",
    "application_process": "application_process",
    "documents_required": "documents_required",
    "department": "department",
}
# same scheme as "free-ug-students-only" (verified: same state/department/text); also dropped in Nimisha's CSV
DROP_SLUGS = {"freeship-ug-students-only"}

HF_ELIG = [
    "eligibility_age_min", "eligibility_age_max", "eligibility_gender", "eligibility_caste",
    "eligibility_income_max", "eligibility_residence", "eligibility_state",
    "eligibility_disability", "eligibility_bpl",
]


def clean_text(s: str | None) -> str:
    """Unescape HTML, turn <br> into newlines, drop tags, collapse whitespace."""
    s = s or ""
    while (u := html.unescape(s)) != s:  # source is double-escaped
        s = u
    s = s.replace("\r", "")
    s = re.sub(r"<br\s*/?>", "\n", s, flags=re.I)
    s = re.sub(r"</?[a-zA-Z][^>]*>", "", s)
    s = re.sub(r"[ \t\xa0]+", " ", s)
    s = re.sub(r"\n\s*\n+", "\n\n", s)
    return s.strip()


def _flat(n) -> str:
    """Flatten a rich-text node tree (children/text) to plain text."""
    if isinstance(n, list):
        return "\n".join(t for t in map(_flat, n) if t)
    if "text" in n:
        return n["text"]
    kids = n.get("children", [])
    inline = all("text" in k or k.get("type") == "link" for k in kids)
    return ("" if inline else "\n").join(_flat(k) for k in kids)


def _text(md: str | None, nodes) -> str:
    """Prefer the *_md field, fall back to flattening the node tree."""
    return clean_text(md) or clean_text(_flat(nodes or []))


def _s(x) -> str:
    return " ".join(str(x).split()) if x else ""


def _label(x) -> str:
    return _s(x.get("label")) if isinstance(x, dict) else _s(x)


def _labels(xs) -> list[str]:
    """Labels from a list of str/{label,value}; trimmed, case-insensitive dedupe."""
    xs = xs if isinstance(xs, list) else [xs]
    out: list[str] = []
    for x in xs:
        lab = _label(x)
        if lab and lab.lower() not in {o.lower() for o in out}:
            out.append(lab)
    return out


def _read(name: str) -> list[dict]:
    return json.loads((RAW / name).read_text(encoding="utf-8"))["items"]


def normalize_url(v) -> str | None:
    """Clean http(s) URL or None; drops blob:/file: values (same rules as Nimisha's normalize_urls.py)."""
    u = str(v or "").strip()
    if u.startswith(("blob:", "file:///")):
        return None
    if m := re.search(r"https?://.+", u):
        return m.group()
    return "https://" + u if u.startswith("www.") else None


def build() -> list[dict]:
    """Return one flat record per unique slug in the list stage."""
    lst: dict[str, dict] = {}
    for x in _read("schemes_list.json"):
        lst.setdefault(x["slug"], x)  # drops duplicate slugs
    for slug in DROP_SLUGS:
        lst.pop(slug, None)
    detail = {x["slug"]: x for x in _read("schemes_detail.json")}
    docs = {x["slug"]: x for x in _read("schemes_documents.json")}
    faqs = {x["slug"]: x for x in _read("schemes_faqs.json")}
    hf = (pd.read_csv(HF_CSV).drop_duplicates("slug").astype(object)
          .where(lambda d: d.notna(), None).set_index("slug").to_dict("index"))

    items = []
    for slug, l in lst.items():
        d = detail.get(slug, {})
        b, c, e = d.get("basicDetails", {}), d.get("schemeContent", {}), d.get("eligibilityCriteria", {})
        h = hf.get(slug, {})
        row = {
            "slug": slug,
            "id": d.get("id"),
            "name": _s(l.get("schemeName") or b.get("schemeName")),
            "level": _s(l.get("level")),
            "states": _labels(l.get("beneficiaryState")),
            "ministry": _label(b.get("nodalMinistryName") or l.get("nodalMinistryName")),
            "department": _label(b.get("nodalDepartmentName")),
            "categories": _labels(b.get("schemeCategory") or l.get("schemeCategory")),
            "sub_categories": _labels(b.get("schemeSubCategory")),
            "tags": _labels(b.get("tags") or l.get("tags")),
            "target_beneficiaries": _labels(b.get("targetBeneficiaries")),
            "scheme_for": _s(b.get("schemeFor") or l.get("schemeFor")),
            "dbt": b.get("dbtScheme"),
            "close_date": b.get("schemeCloseDate") or l.get("schemeCloseDate"),
            "brief_description": clean_text(c.get("briefDescription") or l.get("briefDescription")),
            "description": _text(c.get("detailedDescription_md"), c.get("detailedDescription")),
            "benefits": _text(c.get("benefits_md"), c.get("benefits")),
            "eligibility": _text(e.get("eligibilityDescription_md"), e.get("eligibilityDescription")),
            "exclusions": _text(c.get("exclusions_md"), c.get("exclusions")),
            "application_process": clean_text("\n\n".join(
                f"[{p.get('mode')}]\n{_flat(p.get('process', []))}" for p in d.get("applicationProcess") or [])),
            "documents_required": clean_text(docs.get(slug, {}).get("documentsRequired_md")),
            "faqs": [{"question": _s(f.get("question")), "answer": _text(f.get("answer_md"), f.get("answer"))}
                     for f in faqs.get(slug, {}).get("faqs") or []],
            "references": [{"title": _s(r.get("title")), "url": r.get("url")} for r in c.get("references") or []],
            "official_url": f"https://www.myscheme.gov.in/schemes/{slug}",
            "apply_url": normalize_url(h.get("apply_url")),
            "source": "api" if d else "hf_csv",
            "filled_from_hf": [],
        }
        for col, hcol in HF_TEXT.items():
            if not row[col] and h.get(hcol):
                row[col] = clean_text(h[hcol])
                row["filled_from_hf"].append(col)
        for col in HF_ELIG:
            row[col] = h.get(col)
        for col in ("eligibility_caste", "eligibility_state"):
            if isinstance(row[col], str):
                row[col] = json.loads(row[col])
        items.append(row)
    return items


def load_clean_schemes(rajasthan_only: bool = False) -> list[dict]:
    """Load the cleaned dataset; rajasthan_only keeps schemes for Rajasthan or 'All'."""
    items = json.loads(OUT.read_text(encoding="utf-8"))["items"]
    if rajasthan_only:
        items = [x for x in items if {"Rajasthan", "All"} & set(x["states"])]
    return items
