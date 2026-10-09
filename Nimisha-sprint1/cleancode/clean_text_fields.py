import pandas as pd
import re
import html
import os

INPUT_FILE = "data/processed/schemes_cleaned.csv"
OUTPUT_FILE = "data/processed/schemes_text_cleaned.csv"

df = pd.read_csv(INPUT_FILE)

TEXT_COLUMNS = [
    "name",
    "description",
    "benefits",
    "eligibility_text",
    "application_process",
    "documents_required",
]


def clean_html_text(value):
    if pd.isna(value):
        return value

    text = str(value)

    # Keep decoding until no more changes occur
    for _ in range(100):
        decoded = html.unescape(text)

        if decoded == text:
            break

        text = decoded

    # Remove HTML tags
    text = re.sub(r"<[^>]+>", " ", text)

    # Normalize escaped line breaks
    text = text.replace("\\n", "\n")
    text = text.replace("\\t", " ")

    # Normalize whitespace
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    return text.strip()


print("\n========== TEXT CLEANING ==========")
print("Input records:", len(df))

for column in TEXT_COLUMNS:
    if column in df.columns:
        df[column] = df[column].apply(clean_html_text)

os.makedirs("data/processed", exist_ok=True)

df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)

print("\n========== COMPLETE ==========")
print("Output records:", len(df))
print("Output columns:", len(df.columns))
print("Saved to:", OUTPUT_FILE)