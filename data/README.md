---
language:
  - en
  - ta
  - hi
  - te
license: cc-by-4.0
task_categories:
  - text-classification
  - question-answering
  - text-retrieval
task_ids:
  - document-retrieval
pretty_name: Indian Government Schemes 2025
size_categories:
  - 1K<n<10K
tags:
  - government
  - india
  - schemes
  - welfare
  - eligibility
  - civic-tech
  - govtech
  - msme
  - business
  - agriculture
  - women-empowerment
  - tamil-nadu
  - hindi
annotations_creators:
  - machine-generated
source_datasets:
  - original
multilinguality:
  - monolingual
---

# Indian Government Schemes Dataset 2026

## Dataset Description

The most comprehensive structured dataset of Indian central and state government schemes — 4,693 schemes across all ministries and states, with machine-readable eligibility fields.

Maintained by **[SmartDuke Technologies](https://smartduke.com)** · Coimbatore, Tamil Nadu, India

This dataset powers **[SchemeFit](https://schemefit.com)** — India's government scheme finder for citizens and businesses.

---

## What Makes This Different

Most existing Indian scheme datasets contain raw text paragraphs with no structure. This dataset includes **parsed eligibility fields** enabling programmatic matching:

- ✅ Gender eligibility (`all`, `male`, `female`)
- ✅ Caste category (`SC`, `ST`, `OBC`, `General`)
- ✅ Annual income limits (in rupees)
- ✅ Rural/urban residence requirements
- ✅ State-specific eligibility (array)
- ✅ BPL (Below Poverty Line) flag
- ✅ Disability flag
- ✅ Age min/max

---

## Dataset Stats

| Field | Value |
|---|---|
| Total schemes | 4,693 |
| Female-only schemes | 448 |
| BPL schemes | 157 |
| Tamil Nadu specific | 232 |
| Central govt schemes | ~3,800 |
| State schemes | ~900 |
| Last updated | July 2026 |

---

## Dataset Fields

| Column | Type | Description |
|---|---|---|
| `slug` | string | Unique URL identifier |
| `name` | string | Scheme name in English |
| `description` | string | Brief description |
| `ministry` | string | Nodal ministry |
| `department` | string | Nodal department |
| `state` | string | `Central` or state name |
| `category` | string | Scheme category tags |
| `benefits` | string | What the beneficiary receives |
| `eligibility_text` | string | Raw eligibility paragraph |
| `application_process` | string | How to apply |
| `documents_required` | string | Documents needed |
| `apply_url` | string | Direct application link |
| `official_url` | string | myscheme.gov.in URL |
| `eligibility_age_min` | integer | Minimum age (null = no limit) |
| `eligibility_age_max` | integer | Maximum age (null = no limit) |
| `eligibility_gender` | string | `all`, `male`, or `female` |
| `eligibility_caste` | list | `["SC","ST","OBC","General"]` |
| `eligibility_income_max` | integer | Annual income limit in ₹ |
| `eligibility_residence` | string | `rural`, `urban`, or `both` |
| `eligibility_state` | list | Eligible states or `["All"]` |
| `eligibility_disability` | boolean | Requires disability status |
| `eligibility_bpl` | boolean | Requires BPL status |
| `scraped_at` | timestamp | When data was collected |

---

## Use Cases

- **Eligibility matching engines** — query by user profile to return matching schemes
- **Legal aid and welfare chatbots** — power RAG systems with structured scheme data
- **Research** — analyse welfare scheme coverage, gaps, and distribution across India
- **LLM fine-tuning** — train models on Indian government domain knowledge
- **GovTech applications** — build citizen-facing tools for scheme discovery

---

## Example Usage

```python
from datasets import load_dataset

ds = load_dataset("smartduketech/indian-government-schemes-2025")
df = ds["train"].to_pandas()

# Find all women-only schemes
women_schemes = df[df["eligibility_gender"] == "female"]
print(f"Women-only schemes: {len(women_schemes)}")

# Find schemes for SC/ST with income limit
sc_st = df[df["eligibility_caste"].apply(
    lambda x: any(c in str(x) for c in ["SC", "ST"]) if x else False
)]
print(f"SC/ST schemes: {len(sc_st)}")

# Find Tamil Nadu specific schemes
tn_schemes = df[df["eligibility_state"].apply(
    lambda x: "Tamil Nadu" in str(x) if x else False
)]
print(f"Tamil Nadu schemes: {len(tn_schemes)}")

# Simple eligibility match function
def match_schemes(df, gender="all", state="Tamil Nadu", residence="urban", income=100000):
    matched = df[
        (df["eligibility_gender"].isin([gender, "all"]) | df["eligibility_gender"].isna()) &
        (df["eligibility_income_max"].isna() | (df["eligibility_income_max"] >= income)) &
        (df["eligibility_residence"].isin([residence, "both"]) | df["eligibility_residence"].isna())
    ]
    return matched

results = match_schemes(df, gender="female", state="Tamil Nadu")
print(f"Matched schemes: {len(results)}")
```

---

## Data Source

- **Original source:** [myscheme.gov.in](https://myscheme.gov.in) — Government of India portal maintained by Digital India Corporation under MeitY
- **Structured parsing:** SmartDuke Technologies using rule-based NLP pipeline
- **Collection date:** July 2026

> ⚠️ Always verify scheme details on the official portal before applying. Scheme eligibility and benefits may change. Apply URLs should be confirmed at myscheme.gov.in.

---

## Maintained By

**[SmartDuke Technologies](https://smartduke.com)**
Web development and AI agency · Coimbatore, Tamil Nadu, India

This dataset powers **[SchemeFit](https://schemefit.com)** — India's government scheme finder for citizens and businesses.

---

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — Free to use with attribution.

Please cite: **SmartDuke Technologies · schemefit.com**

---

## Citation

```bibtex
@dataset{smartduketech2026schemes,
  author    = {SmartDuke Technologies},
  title     = {Indian Government Schemes Dataset 2026},
  year      = {2026},
  publisher = {Hugging Face},
  url       = {https://huggingface.co/datasets/smartduketech/indian-government-schemes-2025},
  note      = {Powers SchemeFit (schemefit.com). Original data from myscheme.gov.in}
}
```