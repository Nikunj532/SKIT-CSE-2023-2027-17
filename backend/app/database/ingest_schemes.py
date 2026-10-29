import ast
import asyncio
import logging
import os
from pathlib import Path
import pandas as pd
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings
from app.repositories.scheme_repository import SchemeRepository

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("adhikar_setu.ingest")


def parse_list(val):
    """Safely parse list strings like '["Puducherry"]' or '[]'."""
    if pd.isna(val) or not val:
        return []
    if isinstance(val, list):
        return val
    try:
        parsed = ast.literal_eval(str(val))
        return parsed if isinstance(parsed, list) else []
    except Exception:
        return [str(val)]


def clean_val(val):
    """Clean pandas NaN values for MongoDB insertion."""
    if pd.isna(val):
        return None
    return val


async def run_ingestion():
    """Ingest processed scheme CSV dataset into MongoDB."""
    # Find dataset filepath
    possible_paths = [
        Path("data/processed/schemes_cleaned_final.csv"),
        Path("../data/processed/schemes_cleaned_final.csv"),
        Path("data/processed/schemes_cleaned.csv"),
    ]

    csv_path = None
    for p in possible_paths:
        if p.exists():
            csv_path = p
            break

    if not csv_path:
        logger.error("Could not find scheme CSV dataset file!")
        return

    logger.info("Reading scheme dataset from %s...", csv_path)
    df = pd.read_csv(csv_path)
    logger.info("Loaded %d rows from CSV.", len(df))

    records = []
    for _, row in df.iterrows():
        rec = {
            "slug": str(row.get("slug")),
            "name": str(row.get("name")),
            "description": clean_val(row.get("description")),
            "ministry": clean_val(row.get("ministry")),
            "department": clean_val(row.get("department")),
            "state": clean_val(row.get("state")),
            "category": clean_val(row.get("category")),
            "beneficiary_type": clean_val(row.get("beneficiary_type")),
            "benefits": clean_val(row.get("benefits")),
            "eligibility_text": clean_val(row.get("eligibility_text")),
            "application_process": clean_val(row.get("application_process")),
            "documents_required": clean_val(row.get("documents_required")),
            "apply_url": clean_val(row.get("apply_url_clean")) or clean_val(row.get("apply_url")),
            "official_url": clean_val(row.get("official_url")),
            "eligibility_age_min": float(row.get("eligibility_age_min")) if pd.notna(row.get("eligibility_age_min")) else None,
            "eligibility_age_max": float(row.get("eligibility_age_max")) if pd.notna(row.get("eligibility_age_max")) else None,
            "eligibility_gender": str(row.get("eligibility_gender")).lower() if pd.notna(row.get("eligibility_gender")) else "all",
            "eligibility_caste": parse_list(row.get("eligibility_caste")),
            "eligibility_income_max": float(row.get("eligibility_income_max")) if pd.notna(row.get("eligibility_income_max")) else None,
            "eligibility_residence": clean_val(row.get("eligibility_residence")),
            "eligibility_state": parse_list(row.get("eligibility_state")),
            "eligibility_disability": bool(row.get("eligibility_disability")) if pd.notna(row.get("eligibility_disability")) else False,
            "eligibility_bpl": bool(row.get("eligibility_bpl")) if pd.notna(row.get("eligibility_bpl")) else False,
        }
        records.append(rec)

    client = AsyncIOMotorClient(settings.MONGODB_URI)
    db = client[settings.MONGODB_DB_NAME]
    repo = SchemeRepository(db)

    await repo.ensure_indexes()
    count = await repo.bulk_upsert(records)
    logger.info("Successfully ingested/upserted %d schemes into MongoDB!", count)

    stats = await repo.get_summary_stats()
    logger.info("Database Summary Stats: %s", stats)
    client.close()


if __name__ == "__main__":
    asyncio.run(run_ingestion())
