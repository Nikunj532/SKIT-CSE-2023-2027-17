import logging
from typing import List, Dict, Any, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import ASCENDING, TEXT, IndexModel

logger = logging.getLogger("adhikar_setu.repository")


class SchemeRepository:
    """Repository handling database access for Government Schemes."""

    COLLECTION_NAME = "schemes"

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db[self.COLLECTION_NAME]

    async def ensure_indexes(self) -> None:
        """Create required indexes for fast queries and text search."""
        try:
            indexes = [
                IndexModel([("slug", ASCENDING)], unique=True, name="unique_slug_idx"),
                IndexModel([("state", ASCENDING)], name="state_idx"),
                IndexModel([("category", ASCENDING)], name="category_idx"),
                IndexModel([("eligibility_gender", ASCENDING)], name="gender_idx"),
                IndexModel(
                    [
                        ("name", TEXT),
                        ("description", TEXT),
                        ("category", TEXT),
                        ("eligibility_text", TEXT),
                    ],
                    name="scheme_text_search_idx",
                ),
            ]
            await self.collection.create_indexes(indexes)
            logger.info("MongoDB indexes verified for '%s' collection.", self.COLLECTION_NAME)
        except Exception as e:
            logger.error("Failed to create indexes: %s", str(e))

    async def get_by_slug(self, slug: str) -> Optional[Dict[str, Any]]:
        """Fetch a single scheme by its unique slug."""
        doc = await self.collection.find_one({"slug": slug})
        if doc and "_id" in doc:
            doc["_id"] = str(doc["_id"])
        return doc

    async def search_schemes(
        self,
        query: Optional[str] = None,
        state: Optional[str] = None,
        category: Optional[str] = None,
        gender: Optional[str] = None,
        age: Optional[int] = None,
        skip: int = 0,
        limit: int = 20,
    ) -> Dict[str, Any]:
        """Search and filter government schemes with pagination."""
        filter_dict: Dict[str, Any] = {}

        if query:
            filter_dict["$text"] = {"$search": query}

        if state and state.lower() != "all":
            filter_dict["$or"] = [
                {"state": {"$regex": f"^{state}$", "$options": "i"}},
                {"state": "All India"},
                {"eligibility_state": {"$regex": f"^{state}$", "$options": "i"}},
            ]

        if category:
            filter_dict["category"] = {"$regex": category, "$options": "i"}

        if gender and gender.lower() in ("male", "female", "transgender"):
            filter_dict["eligibility_gender"] = {"$in": [gender.lower(), "all", None]}

        if age is not None:
            filter_dict["$and"] = [
                {"$or": [{"eligibility_age_min": {"$lte": age}}, {"eligibility_age_min": None}]},
                {"$or": [{"eligibility_age_max": {"$gte": age}}, {"eligibility_age_max": None}]},
            ]

        total = await self.collection.count_documents(filter_dict)
        cursor = self.collection.find(filter_dict).skip(skip).limit(limit)
        
        schemes = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            schemes.append(doc)

        return {
            "total": total,
            "page": (skip // limit) + 1 if limit > 0 else 1,
            "limit": limit,
            "schemes": schemes,
        }

    async def bulk_upsert(self, schemes: List[Dict[str, Any]]) -> int:
        """Bulk upsert schemes dataset by slug."""
        if not schemes:
            return 0
        
        from pymongo import UpdateOne
        operations = [
            UpdateOne({"slug": s["slug"]}, {"$set": s}, upsert=True)
            for s in schemes if "slug" in s and s["slug"]
        ]

        if not operations:
            return 0

        result = await self.collection.bulk_write(operations)
        return result.upserted_count + result.modified_count

    async def get_summary_stats(self) -> Dict[str, Any]:
        """Get database summary statistics."""
        total_schemes = await self.collection.count_documents({})
        states = await self.collection.distinct("state")
        categories = await self.collection.distinct("category")
        return {
            "total_schemes": total_schemes,
            "states_count": len([s for s in states if s]),
            "categories_count": len([c for c in categories if c]),
        }
