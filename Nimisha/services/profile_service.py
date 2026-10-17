import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Optional

from Nimisha.schemas.profile import ProfileCreate, ProfileResponse, ProfileUpdate


DATA_FILE = Path("data/profiles.json")


class ProfileService:
    def __init__(self, data_file: Path = DATA_FILE):
        self.data_file = data_file
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        if not self.data_file.parent.exists():
            self.data_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.data_file.exists():
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump({}, f)

    def _read_profiles(self) -> Dict[str, dict]:
        self._ensure_file_exists()
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return {}

    def _write_profiles(self, profiles: Dict[str, dict]) -> None:
        self._ensure_file_exists()
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(profiles, f, indent=2, ensure_ascii=False)

    def create_profile(self, profile_in: ProfileCreate) -> ProfileResponse:
        profiles = self._read_profiles()
        profile_id = f"prof_{uuid.uuid4().hex[:8]}"
        now = datetime.now(timezone.utc).isoformat()

        profile_data = profile_in.model_dump()
        profile_data.update({
            "profile_id": profile_id,
            "created_at": now,
            "updated_at": now
        })

        profiles[profile_id] = profile_data
        self._write_profiles(profiles)
        return ProfileResponse(**profile_data)

    def get_profile(self, profile_id: str) -> Optional[ProfileResponse]:
        profiles = self._read_profiles()
        if profile_id not in profiles:
            return None
        return ProfileResponse(**profiles[profile_id])

    def update_profile(self, profile_id: str, profile_in: ProfileUpdate) -> Optional[ProfileResponse]:
        profiles = self._read_profiles()
        if profile_id not in profiles:
            return None

        stored_data = profiles[profile_id]
        update_data = profile_in.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            if value is not None:
                stored_data[key] = value

        stored_data["updated_at"] = datetime.now(timezone.utc).isoformat()
        profiles[profile_id] = stored_data
        self._write_profiles(profiles)
        return ProfileResponse(**stored_data)

    def clear_all(self) -> None:
        """Utility for test isolation."""
        self._write_profiles({})
