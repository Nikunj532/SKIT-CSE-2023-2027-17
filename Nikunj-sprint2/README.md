# Sprint 2: Data Cleaning & Normalization (Nikunj, Member 1)

Builds one flat, cleaned dataset from the Sprint 1 myScheme data (list + detail + documents + faqs),
using the HF CSV (`data/raw/Schemes.csv`) to fill gaps and to add eligibility fields and `apply_url`.

## Run / use
- Build: `python -m backend.cleaning.run_cleaning`  ->  `data/processed/myscheme/schemes_clean.json` (~39 MB)
- Load (teammates): `from backend.cleaning import load_clean_schemes`
  - `load_clean_schemes()` -> list of dicts (5086)
  - `load_clean_schemes(rajasthan_only=True)` -> schemes whose `states` include Rajasthan or All (1057)

## What it does
- Base = unique slugs of the list stage (5089 ids; 2 duplicate slugs dropped -> 5087; duplicate scheme `freeship-ug-students-only` dropped -> 5086)
- Joins detail, documents, faqs on `slug`; rich-text trees are flattened to plain text
- Text cleaning: double-escaped HTML entities, `<br>`/tags, `\r`, extra whitespace
- 16 schemes with no API detail (`source = "hf_csv"`) are filled from the HF CSV; `filled_from_hf` lists the fields taken from HF (395 schemes had at least one field filled)
- From HF CSV: eligibility fields (age, gender, caste, income, residence, state, disability, bpl) and `apply_url` (normalized: blob:/file: dropped, wrapper stripped)

## Done checklist
- [x] Duplicate slugs and duplicate scheme removed
- [x] Text fields cleaned (no leftover entities/tags)
- [x] 16 no-detail schemes filled from HF CSV
- [x] HF eligibility fields and apply_url merged
- [x] Rajasthan + All subset via `load_clean_schemes(rajasthan_only=True)`
- [x] Output schema documented in `Nikunj-sprint1/api_notes.md` (Sprint 2 section)
- [ ] Merge `origin/main`, push, PR to `main`

## Known limitations
- Eligibility fields and `apply_url` exist only for slugs present in the HF CSV (4693); `eligibility_age_min` is empty for 4035 schemes. S4 will derive structured conditions from the `eligibility` text.
- `close_date` is present for only 56 schemes.
- `fhdfh` and `fhodfhr` (Rajasthan) have the same name but different content; both kept.
- Existing `data/processed/*.csv` (HF-based) were not modified. `backend/app/database/ingest_schemes.py` still reads `schemes_cleaned_final.csv`; moving it to `schemes_clean.json` is planned for S3 together with the backend owner.
