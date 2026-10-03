# api_notes.md: myScheme ingestion (Sprint 1, Nikunj)

Source: https://www.myscheme.gov.in (public API, no auth, robots.txt disallows only /404).
Politeness: 1 sec delay between calls, retry with backoff on 429/5xx/timeouts.
Run from repo root: `python -m backend.ingestion.run_ingestion [--stage list|detail|documents|faqs]`

## 1. APIs used

| Stage | Endpoint | Key |
|---|---|---|
| list | `GET /api/apisetu/search/schemes?lang=en&q=[]&keyword=&sort=<sort>&from=<n>&size=100` | pagination |
| detail | `GET /api/apisetu/schemes?slug=<slug>&lang=en` | slug |
| documents | `GET /api/apisetu/schemes/<_id>/documents?lang=en` | detail `_id` |
| faqs | `GET /api/apisetu/schemes/<_id>/faqs?lang=en` | detail `_id` |

Not fetched: `applicationchannel` (different host; mode/url already in detail `applicationProcess`).

## 2. Findings (read before using the data)

- Total schemes: 5089 (list). Single paginated pass skips/duplicates items (4880 unique), so list stage runs multiple sort passes (`schemename-asc`, `schemename-desc`, default) and merges by `id`. Result: 5089 unique ids.
- **Join key across all files = `slug`.** List `id` and detail `_id` are DIFFERENT values.
- 5089 ids but 5087 unique slugs:
  - `psnjsy`: 2 list entries, same scheme (Rajasthan), same detail.
  - `tufs`: 2 different schemes share the slug (Puducherry "Technology Upgradation Fund Scheme" and Rajasthan "Transgender Utthan Kosh"). Detail API returns the Rajasthan one; Puducherry TUFS detail is not available. Known limitation, irrelevant for Rajasthan.
- Detail/documents/faqs are fetched per unique slug (5087). `schemes_list.json` keeps all 5089 raw entries; dedupe happens in S2.
- Batching is not supported (comma-separated or repeated slug returns null / only the first).
- Rajasthan filter: use `beneficiaryState` (values include "All" and "Rajasthan"), done in S2, not at ingestion.
- Rich-text fields have a tree version and an `_md` version; use `_md` for embeddings (S5).
- Detail has no structured eligibility rules, only free text (`eligibilityDescription_md`).

## 3. Output files (data contract, do not change without telling the team)

All in `data/raw/myscheme/`, UTF-8, same envelope:
`{"source": "myscheme.gov.in", "fetched_at": ISO-UTC, "total": N, "items": [...]}`
(detail/documents/faqs envelopes also have `"stage"` and `"count"`.)

| File | Items | In git? |
|---|---|---|
| `schemes_list.json` | 5089, flat `{id, **fields}` | yes |
| `schemes_detail.json` | 5087, `{id (=_id), slug, **data.en}` | no (large, gitignored) |
| `schemes_documents.json` | 5087, `{id, slug, documentsRequired_md, documents_required}` | no |
| `schemes_faqs.json` | 5087, `{id, slug, faqs[{question, answer, answer_md}]}` | no |

List item fields: id, beneficiaryState, briefDescription, level, nodalMinistryName, priority, schemeCategory, schemeCloseDate, schemeFor, schemeName, schemeShortTitle, slug, tags.

Detail item (`data.en`): basicDetails, schemeContent (benefits, briefDescription, detailedDescription, exclusions, references; each with `_md`), eligibilityCriteria, applicationProcess, schemeDefinitions.

A scheme with no documents or FAQs gets an empty record (only id and slug).

## 4. Loading data (no API hit)

```python
from backend.ingestion.myscheme import load_schemes
from backend.ingestion.myscheme_detail import (
    load_scheme_details, load_scheme_documents, load_scheme_faqs, get_scheme)

schemes = load_schemes()          # list items
scheme = get_scheme("rtif")       # {"slug", "detail", "documents", "faqs"}
```

Raw detail/documents/faqs files are not in git. Generate them with:
`python -m backend.ingestion.run_ingestion --stage detail` then `--stage documents` then `--stage faqs`
(~2.5 hours each, resumable; Ctrl+C and re-run continues).

## 5. Samples

See `sample_outputs/` (small samples only).