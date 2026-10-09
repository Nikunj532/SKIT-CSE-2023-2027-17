import pandas as pd
import re
import os

INPUT_FILE = "data/processed/schemes_text_cleaned.csv"
OUTPUT_FILE = "data/processed/schemes_cleaned_final.csv"

df = pd.read_csv(INPUT_FILE)


def normalize_apply_url(value):
    if pd.isna(value):
        return pd.NA

    url = str(value).strip()

    if not url:
        return pd.NA

    # Browser-generated blob URL
    if url.startswith("blob:"):
        return pd.NA

    # Local file path from another computer
    if url.startswith("file:///"):
        return pd.NA

    # Extract real HTTPS URL from chrome-extension wrapper
    match = re.search(r"(https?://.+)", url)

    if match:
        return match.group(1)

    # Normal URL without protocol
    if url.startswith("www."):
        return "https://" + url

    # Already valid HTTP/HTTPS
    if url.startswith(("http://", "https://")):
        return url

    return pd.NA


df["apply_url_clean"] = df["apply_url"].apply(normalize_apply_url)

os.makedirs("data/processed", exist_ok=True)

df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)

print("\n========== URL NORMALIZATION ==========")

print("Total records:", len(df))

print(
    "Original apply_url values:",
    df["apply_url"].notna().sum()
)

print(
    "Clean apply_url values:",
    df["apply_url_clean"].notna().sum()
)

print(
    "Unavailable apply_url values:",
    df["apply_url_clean"].isna().sum()
)

print("\n========== NORMALIZED URL CHECK ==========")

invalid = (
    df["apply_url_clean"].notna()
    &
    ~df["apply_url_clean"]
    .astype(str)
    .str.startswith(("http://", "https://"))
)

print("Invalid normalized URLs:", invalid.sum())

print("\nSaved to:")
print(OUTPUT_FILE)

print("\n========== COMPLETE ==========")