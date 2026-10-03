import pandas as pd
import re

INPUT_FILE = "data/processed/schemes_text_cleaned.csv"

df = pd.read_csv(INPUT_FILE)

TEXT_COLUMNS = [
    "name",
    "description",
    "benefits",
    "eligibility_text",
    "application_process",
    "documents_required"
]

HTML_PATTERN = re.compile(r"<[^>]+>")

print("\n========== TEXT CLEANING VERIFICATION ==========")
print("Total records:", len(df))

print("\n========== HTML TAGS ==========")

total_html = 0

for column in TEXT_COLUMNS:
    count = (
        df[column]
        .fillna("")
        .astype(str)
        .apply(lambda x: bool(HTML_PATTERN.search(x)))
        .sum()
    )

    total_html += count
    print(f"{column:25} remaining HTML: {count}")

print("\nTotal fields containing HTML:", total_html)


print("\n========== HTML ENCODED ENTITIES ==========")

ENTITY_PATTERN = re.compile(
    r"&amp;|&quot;|&#39;|&nbsp;|&lt;|&gt;"
)

total_entities = 0

for column in TEXT_COLUMNS:
    count = (
        df[column]
        .fillna("")
        .astype(str)
        .apply(lambda x: bool(ENTITY_PATTERN.search(x)))
        .sum()
    )

    total_entities += count
    print(f"{column:25} remaining entities: {count}")

print("\nTotal fields containing encoded entities:", total_entities)


print("\n========== MISSING VALUES ==========")

for column in TEXT_COLUMNS:
    missing = df[column].isna().sum()
    print(f"{column:25} missing: {missing}")


print("\n========== ROW / COLUMN CHECK ==========")
print("Rows   :", len(df))
print("Columns:", len(df.columns))


print("\n========== COMPLETE ==========")