import pandas as pd

INPUT_FILE = "data/processed/schemes_text_cleaned.csv"

df = pd.read_csv(INPUT_FILE)

print("\n========== APPLY URL REVIEW ==========")

invalid_mask = (
    df["apply_url"].fillna("").astype(str).str.strip().ne("")
    &
    ~df["apply_url"]
    .fillna("")
    .astype(str)
    .str.strip()
    .str.startswith(("http://", "https://"))
)

invalid_urls = df[invalid_mask]

print("Invalid apply URLs:", len(invalid_urls))

for i, (_, row) in enumerate(invalid_urls.iterrows(), start=1):
    print("\n" + "=" * 80)
    print(f"REVIEW #{i}")
    print("=" * 80)

    print("Slug         :", row["slug"])
    print("Scheme       :", row["name"])
    print("Apply URL    :", row["apply_url"])
    print("Official URL :", row["official_url"])

print("\n========== COMPLETE ==========")