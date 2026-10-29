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

ENTITY_PATTERN = re.compile(
    r"&amp;|&quot;|&#39;|&nbsp;|&lt;|&gt;"
)

print("\n========== REMAINING ENCODED ENTITY ==========")

found = 0

for _, row in df.iterrows():
    for column in TEXT_COLUMNS:
        value = "" if pd.isna(row[column]) else str(row[column])

        if ENTITY_PATTERN.search(value):
            found += 1

            print("\n----------------------------------------")
            print("Slug       :", row["slug"])
            print("Scheme     :", row["name"])
            print("Column     :", column)
            print("Value      :", value)

print("\nTotal remaining fields:", found)
print("\n========== COMPLETE ==========")