import pandas as pd
import re

INPUT_FILE = "data/raw/Schemes.csv"
OUTPUT_FILE = "data/processed/schemes_cleaned.csv"


# --------------------------------------------------
# 1. Load dataset
# --------------------------------------------------

df = pd.read_csv(INPUT_FILE)

print(f"Original rows: {len(df)}")
print(f"Original columns: {len(df.columns)}")


# --------------------------------------------------
# 2. Normalize missing-value representations
# --------------------------------------------------

MISSING_VALUES = [
    "",
    " ",
    "NA",
    "N/A",
    "na",
    "n/a",
    "None",
    "none",
    "NULL",
    "null",
    "NaN",
    "nan"
]

df = df.replace(MISSING_VALUES, pd.NA)


# --------------------------------------------------
# 3. Clean text columns
# --------------------------------------------------

text_columns = [
    "slug",
    "name",
    "description",
    "ministry",
    "department",
    "state",
    "category",
    "beneficiary_type",
    "benefits",
    "eligibility_text",
    "application_process",
    "documents_required",
    "apply_url",
    "official_url",
    "eligibility_gender",
    "eligibility_caste",
    "eligibility_residence",
    "eligibility_state",
    "scraped_at"
]


def clean_text(value):
    if pd.isna(value):
        return value

    value = str(value)

    # Replace escaped newlines/tabs
    value = value.replace("\\n", "\n")
    value = value.replace("\\t", " ")

    # Remove excessive whitespace
    value = re.sub(r"[ \t]+", " ", value)

    # Clean excessive blank lines
    value = re.sub(r"\n\s*\n+", "\n\n", value)

    return value.strip()


for column in text_columns:
    if column in df.columns:
        df[column] = df[column].apply(clean_text)


# --------------------------------------------------
# 4. Normalize gender
# --------------------------------------------------

if "eligibility_gender" in df.columns:
    df["eligibility_gender"] = (
        df["eligibility_gender"]
        .astype("string")
        .str.strip()
        .str.lower()
    )


# --------------------------------------------------
# 5. Normalize residence
# --------------------------------------------------

if "eligibility_residence" in df.columns:
    df["eligibility_residence"] = (
        df["eligibility_residence"]
        .astype("string")
        .str.strip()
        .str.lower()
    )


# --------------------------------------------------
# 6. Normalize numeric eligibility fields
# --------------------------------------------------

numeric_columns = [
    "eligibility_age_min",
    "eligibility_age_max",
    "eligibility_income_max"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )


# --------------------------------------------------
# 7. Remove exact duplicate rows
# --------------------------------------------------

before = len(df)

df = df.drop_duplicates()

after = len(df)

print(f"Exact duplicates removed: {before - after}")


# --------------------------------------------------
# 8. Check duplicate identifiers
# --------------------------------------------------

print(
    "Duplicate slugs:",
    df["slug"].duplicated().sum()
)

print(
    "Duplicate names:",
    df["name"].duplicated().sum()
)


# --------------------------------------------------
# 9. Validate gender values
# --------------------------------------------------

valid_genders = {
    "all",
    "male",
    "female"
}

invalid_gender = df[
    ~df["eligibility_gender"].isin(valid_genders)
    & df["eligibility_gender"].notna()
]

print(
    "Invalid gender values:",
    len(invalid_gender)
)


# --------------------------------------------------
# 10. Validate residence values
# --------------------------------------------------

valid_residence = {
    "rural",
    "urban",
    "both"
}

invalid_residence = df[
    ~df["eligibility_residence"].isin(valid_residence)
    & df["eligibility_residence"].notna()
]

print(
    "Invalid residence values:",
    len(invalid_residence)
)


# --------------------------------------------------
# 11. Create processed directory
# --------------------------------------------------

import os

os.makedirs(
    "data/processed",
    exist_ok=True
)


# --------------------------------------------------
# 12. Save cleaned dataset
# --------------------------------------------------

df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)


# --------------------------------------------------
# 13. Final report
# --------------------------------------------------

print("\n========== CLEANING COMPLETE ==========")

print(f"Final rows: {len(df)}")
print(f"Final columns: {len(df.columns)}")
print(f"Saved to: {OUTPUT_FILE}")

print("\nMissing values after cleaning:")

print(
    df.isna()
    .sum()
    .sort_values(ascending=False)
)