"""Sprint 3: load schemes_clean.json into MongoDB (collection `schemes`, upsert by slug).

Run (repo root): python -m backend.mongo.load_schemes [--dry-run]
Config: MONGODB_URI and MONGODB_DB_NAME env vars (read via database.mongodb).

Each document = every field of schemes_clean.json (unchanged) + compat fields used by
backend/app (state, category, beneficiary_type, eligibility_text), so its API keeps working.
"""
import argparse
from pymongo import ASCENDING, TEXT, IndexModel, MongoClient, UpdateOne

from backend.cleaning import load_clean_schemes
from database.mongodb import get_database_name, get_mongodb_uri

COLLECTION = "schemes"
BATCH = 500

# First five = same names/specs as SchemeRepository.ensure_indexes (backend/app/repositories/
# scheme_repository.py); keep in sync. Last three are new (Sprint 3).
INDEXES = [
    IndexModel([("slug", ASCENDING)], unique=True, name="unique_slug_idx"),
    IndexModel([("state", ASCENDING)], name="state_idx"),
    IndexModel([("category", ASCENDING)], name="category_idx"),
    IndexModel([("eligibility_gender", ASCENDING)], name="gender_idx"),
    IndexModel(
        [("name", TEXT), ("description", TEXT), ("category", TEXT), ("eligibility_text", TEXT)],
        name="scheme_text_search_idx",
    ),
    IndexModel([("states", ASCENDING)], name="states_idx"),
    IndexModel([("categories", ASCENDING)], name="categories_idx"),
    IndexModel([("level", ASCENDING)], name="level_idx"),
]


def to_mongo_doc(item: dict) -> dict:
    """Return the scheme with the extra flat fields backend/app expects."""
    states = item.get("states") or []
    doc = dict(item)
    doc["state"] = "All India" if "All" in states else (states[0] if states else None)
    doc["category"] = ", ".join(item.get("categories") or []) or None
    doc["beneficiary_type"] = ", ".join(item.get("target_beneficiaries") or []) or None
    doc["eligibility_text"] = item.get("eligibility") or None
    return doc


def load_schemes_to_mongo(docs: list[dict], uri: str, db_name: str) -> dict:
    """Create indexes and upsert docs by slug. Returns {'loaded', 'in_collection'}."""
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    try:
        coll = client[db_name][COLLECTION]
        coll.create_indexes(INDEXES)
        for i in range(0, len(docs), BATCH):
            ops = [UpdateOne({"slug": d["slug"]}, {"$set": d}, upsert=True) for d in docs[i:i + BATCH]]
            coll.bulk_write(ops, ordered=False)
        return {"loaded": len(docs), "in_collection": coll.count_documents({})}
    finally:
        client.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--dry-run", action="store_true", help="map documents only, do not touch MongoDB")
    args = parser.parse_args()

    docs = [to_mongo_doc(x) for x in load_clean_schemes()]
    assert len({d["slug"] for d in docs}) == len(docs), "duplicate slugs"
    print(f"mapped {len(docs)} schemes")
    if args.dry_run:
        d = docs[0]
        print({k: d[k] for k in ("slug", "name", "state", "category", "beneficiary_type", "states", "categories")})
        return
    print(f"loading into db '{get_database_name()}', collection '{COLLECTION}'")
    print(load_schemes_to_mongo(docs, get_mongodb_uri(), get_database_name()))


if __name__ == "__main__":
    main()
