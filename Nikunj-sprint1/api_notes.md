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
| `schemes_detail.json` | 5071, `{id (=_id), slug, **data.en}` | zip only (`myscheme_detail_documents_faqs.zip`) |
| `schemes_documents.json` | 5071, `{id, slug, documentsRequired_md, documents_required}` | zip only (`myscheme_detail_documents_faqs.zip`) |
| `schemes_faqs.json` | 5071, `{id, slug, faqs[{question, answer, answer_md}]}` | zip only (`myscheme_detail_documents_faqs.zip`) |

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

Raw detail/documents/faqs are in git only as `data/raw/myscheme/myscheme_detail_documents_faqs.zip`; unzip it inside `data/raw/myscheme/`. To regenerate instead, run:
`python -m backend.ingestion.run_ingestion --stage detail` then `--stage documents` then `--stage faqs`
(~2.5 hours each, resumable; Ctrl+C and re-run continues).

## 5. Samples

See `sample_outputs/` (small samples only).
## 6. Final run numbers (04/10/2026)

| Stage | Items | With content |
|---|---|---|
| list | 5089 (5087 unique slugs) | all |
| detail | 5071 | all |
| documents | 5071 | 4678 have `documentsRequired_md` |
| faqs | 5071 | 5058 have FAQs |

- Same 5071 slugs in detail, documents and faqs. Missing 16 slugs: detail API returns `data: null` (permanent), so documents/faqs were skipped for them. All 16 are present in the HF CSV (`data/raw/Schemes.csv`, same slug), use it to fill their text in S2.
- File sizes (unzipped; only the zip is in git): detail 52 MB, documents 7.3 MB, faqs 25 MB.
- Observed speed: ~100 schemes per 2.7 min (1 sec delay + network), ~2.3 h per stage.
