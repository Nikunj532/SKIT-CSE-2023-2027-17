import json
from pathlib import Path

from backend.schemas.scheme import Scheme


DATA_PATH = Path("data/processed/schemes.json")


def load_schemes() -> list[Scheme]:
    if not DATA_PATH.exists():
        return []
    with open(DATA_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)

    return [Scheme(**scheme) for scheme in data]


def get_all_schemes() -> list[Scheme]:
    return load_schemes()