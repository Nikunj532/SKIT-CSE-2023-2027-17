"""Build data/processed/myscheme/schemes_clean.json. Run: python -m backend.cleaning.run_cleaning"""
import json
from datetime import datetime, timezone

import pandas as pd

from .clean_schemes import OUT, build


def main() -> None:
    items = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    payload = {"source": "myscheme.gov.in + HF Schemes.csv",
               "built_at": datetime.now(timezone.utc).isoformat(),
               "total": len(items), "items": items}
    OUT.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    df = pd.DataFrame(items)
    print("total", len(df), df["source"].value_counts().to_dict())
    print("filled_from_hf:", int(df["filled_from_hf"].str.len().gt(0).sum()))


if __name__ == "__main__":
    main()
