import pandas as pd
import re

INPUT_FILE = "data/processed/schemes_cleaned.csv"

df = pd.read_csv(INPUT_FILE)

print("\n========== TEXT QUALITY CHECK ==========")
print("Total records:", len(df))

TEXT_COLUMNS = [
    "name",
    "description",
    "benefits",
    "eligibility_text",
    "application_process",
    "documents_required"
]

print("\n========== MISSING VALUES ==========")

for column in TEXT_COLUMNS:
    missing = df[column].isna().sum()
    empty = (
        df[column]
        .fillna("")
        .astype(str)
        .str.strip()
        .eq("")
        .sum()
    )

    print(
        f"{column:25} "
        f"missing={missing:4} "
        f"empty={empty:4}"
    )


print("\n========== VERY SHORT TEXT ==========")

for column in TEXT_COLUMNS:
    text_length = (
        df[column]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.len()
    )

    short_count = (text_length < 20).sum()

    print(
        f"{column:25} "
        f"<20 characters: {short_count}"
    )


print("\n========== HTML / ENCODING ARTIFACTS ==========")

HTML_PATTERN = re.compile(r"<[^>]+>")

for column in TEXT_COLUMNS:
    html_count = (
        df[column]
        .fillna("")
        .astype(str)
        .apply(lambda x: bool(HTML_PATTERN.search(x)))
        .sum()
    )

    encoded_count = (
        df[column]
        .fillna("")
        .astype(str)
        .str.contains(
            r"&amp;|&quot;|&#39;|&nbsp;",
            regex=True,
            na=False
        )
        .sum()
    )

    print(
        f"{column:25} "
        f"HTML={html_count:4} "
        f"encoded_entities={encoded_count:4}"
    )


print("\n========== URL CHECK ==========")

for column in ["apply_url", "official_url"]:
    invalid = (
        df[column]
        .fillna("")
        .astype(str)
        .str.strip()
        .ne("")
        &
        ~df[column]
        .fillna("")
        .astype(str)
        .str.startswith(("http://", "https://"))
    ).sum()

    print(f"{column:25} invalid URLs: {invalid}")


print("\n========== TEXT LENGTH SUMMARY ==========")

for column in TEXT_COLUMNS:
    lengths = (
        df[column]
        .fillna("")
        .astype(str)
        .str.len()
    )

    print(
        f"\n{column}"
        f"\n  Minimum : {lengths.min()}"
        f"\n  Average : {lengths.mean():.1f}"
        f"\n  Maximum : {lengths.max()}"
    )


print("\n========== COMPLETE ==========")