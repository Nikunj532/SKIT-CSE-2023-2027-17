# Sprint 1: Ingestion Pipeline (Nikunj, Member 1)

Goal: scheme data collected automatically from myScheme.gov.in (5089 schemes, no state filter; Rajasthan filter is done in S2).

## How to run (from repo root)

```bash
pip install -r requirements.txt
python -m backend.ingestion.run_ingestion                    # list (~1 min)
python -m backend.ingestion.run_ingestion --stage detail     # ~2.5 h, resumable
python -m backend.ingestion.run_ingestion --stage documents  # ~2.5 h, resumable
python -m backend.ingestion.run_ingestion --stage faqs       # ~2.5 h, resumable
```

Ctrl+C is safe; re-running continues from the checkpoint. Delay is 1 sec per call (government site).

## Code

`backend/ingestion/`: `config.py` (paths, URLs, rate limit), `fetcher.py` (rate-limited client with retry), `myscheme.py` (list stage + loader), `myscheme_detail.py` (detail/documents/faqs stages + loaders), `run_ingestion.py` (CLI).

## Output (data contract)

See `api_notes.md`. Join key across all files is `slug` (not `id`). Only `schemes_list.json` is in git; detail/documents/faqs files are generated locally.

## Done checklist

- [x] List stage: 5089 unique ids (multi-pass fetch fixes API pagination gaps)
- [x] Detail, documents, faqs stages with resumable checkpoint
- [x] CLI with `--stage`
- [x] `api_notes.md` (APIs, findings, contract)
- [x] Sample outputs in `sample_outputs/`
- [x] Detail stage run complete (5071 / 5087)
- [x] Documents stage run complete (5071 / 5087, 4678 with text)
- [x] Faqs stage run complete (5071 / 5087, 5058 with FAQs)
- [ ] Merge `origin/main`, push, PR to `main`

## Known limitations

- 2 duplicate slugs in the list (`psnjsy`, `tufs`); Puducherry "TUFS" detail is not available.
- Some schemes have no detail in the API (`data: null`); they are listed in `schemes_detail_failed.json` and skipped in documents/faqs.- 16 slugs have no detail in the API (`data: null`, permanent, listed in `schemes_detail_failed.json`): 12 central ("All"), 2 Dadra & Nagar Haveli and Daman & Diu, 2 Himachal Pradesh. Their documents/faqs were skipped. All 16 exist in the HF dataset CSV (`data/raw/Schemes.csv`), so S2 can fill their text from it by slug.
