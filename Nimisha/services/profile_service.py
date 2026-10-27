import json
import uuid
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

from Nimisha.schemas.profile import (
    ProfileCreate,
    ProfileResponse,
    ProfileUpdate,
    ProfileInDB,
    PROFILES_COLLECTION,
)

logger = logging.getLogger("adhikar_setu.profile_service")

DATA_FILE = Path("data/profiles.json")


class ProfileService:
    """
    Profile Service managing citizen profile persistence.
    Supports MongoDB persistence when configured/available, and safely
    falls back to JSON file persistence for local development and offline environments.
    """

    def __init__(self, data_file: Path = DATA_FILE, mongo_db=None):
        self.data_file = Path(data_file)
        self.mongo_db = mongo_db

        # If mongo_db not explicitly provided, attempt to connect if available
        if self.mongo_db is None and str(data_file) == str(DATA_FILE):
            try:
                from database.mongodb import get_sync_db
                self.mongo_db = get_sync_db()
            except Exception:
                self.mongo_db = None

        if self.mongo_db is not None:
            self.backend_type = "mongodb"
            self.collection = self.mongo_db[PROFILES_COLLECTION]
        else:
            self.backend_type = "json_file"
            self.collection = None
            self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        if self.backend_type != "json_file":
            return
        if not self.data_file.parent.exists():
            self.data_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.data_file.exists():
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump({}, f)

    def _read_profiles_file(self) -> Dict[str, dict]:
        self._ensure_file_exists()
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return {}

    def _write_profiles_file(self, profiles: Dict[str, dict]) -> None:
        self._ensure_file_exists()
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(profiles, f, indent=2, ensure_ascii=False)

    def create_profile(self, profile_in: ProfileCreate) -> ProfileResponse:
        """
        Creates a new citizen profile.
        Persists into MongoDB or JSON file.
        """
        profile_id = f"prof_{uuid.uuid4().hex[:8]}"
        now = datetime.now(timezone.utc).isoformat()

        profile_data = profile_in.model_dump()
        profile_data.update({
            "profile_id": profile_id,
            "created_at": now,
            "updated_at": now
        })

        if self.backend_type == "mongodb" and self.collection is not None:
            doc = dict(profile_data)
            result = self.collection.insert_one(doc)
            profile_data["_id"] = str(result.inserted_id)
            return ProfileResponse(**profile_data)
        else:
            profiles = self._read_profiles_file()
            profiles[profile_id] = profile_data
            self._write_profiles_file(profiles)
            return ProfileResponse(**profile_data)

    def get_profile(self, profile_id: str) -> Optional[ProfileResponse]:
        """
        Retrieves an existing citizen profile by its business profile_id.
        """
        if self.backend_type == "mongodb" and self.collection is not None:
            doc = self.collection.find_one({"profile_id": profile_id})
            if not doc:
                return None
            doc["_id"] = str(doc.get("_id", ""))
            return ProfileResponse(**doc)
        else:
            profiles = self._read_profiles_file()
            if profile_id not in profiles:
                return None
            return ProfileResponse(**profiles[profile_id])

    def update_profile(self, profile_id: str, profile_in: ProfileUpdate) -> Optional[ProfileResponse]:
        """
        Updates fields of an existing citizen profile.
        """
        update_data = profile_in.model_dump(exclude_unset=True)
        # Filter out explicit None values
        clean_updates = {k: v for k, v in update_data.items() if v is not None}
        if not clean_updates:
            return self.get_profile(profile_id)

        clean_updates["updated_at"] = datetime.now(timezone.utc).isoformat()

        if self.backend_type == "mongodb" and self.collection is not None:
            doc = self.collection.find_one_and_update(
                {"profile_id": profile_id},
                {"$set": clean_updates},
                return_document=True
            )
            if not doc:
                return None
            doc["_id"] = str(doc.get("_id", ""))
            return ProfileResponse(**doc)
        else:
            profiles = self._read_profiles_file()
            if profile_id not in profiles:
                return None

            stored_data = profiles[profile_id]
            stored_data.update(clean_updates)
            profiles[profile_id] = stored_data
            self._write_profiles_file(profiles)
            return ProfileResponse(**stored_data)

    def list_profiles(self, skip: int = 0, limit: int = 20) -> List[ProfileResponse]:
        """
        Lists stored citizen profiles with pagination.
        """
        if self.backend_type == "mongodb" and self.collection is not None:
            cursor = self.collection.find().skip(skip).limit(limit)
            results = []
            for doc in cursor:
                doc["_id"] = str(doc.get("_id", ""))
                results.append(ProfileResponse(**doc))
            return results
        else:
            profiles = self._read_profiles_file()
            items = list(profiles.values())[skip:skip + limit]
            return [ProfileResponse(**p) for p in items]

    def clear_all(self) -> None:
        """Utility for test isolation."""
        if self.backend_type == "mongodb" and self.collection is not None:
            self.collection.delete_many({})
        else:
            self._write_profiles_file({})
