import pandas as pd

INPUT_FILE = "data/processed/schemes_cleaned_final.csv"

df = pd.read_csv(INPUT_FILE)

print("\n========== FINAL DATASET AUDIT ==========")

print("Rows    :", len(df))
print("Columns :", len(df.columns))

print("\n========== DUPLICATES ==========")

print("Duplicate rows :", df.duplicated().sum())
print("Duplicate slugs:", df["slug"].duplicated().sum())

print("\n========== REQUIRED COLUMNS ==========")

required_columns = [
    "slug",
    "name",
    "description",
    "benefits",
    "eligibility_text",
    "application_process",
    "documents_required",
    "official_url",
    "apply_url_clean",
    "eligibility_age_min",
    "eligibility_age_max",
    "eligibility_gender",
    "eligibility_caste",
    "eligibility_income_max",
    "eligibility_residence",
    "eligibility_state",
    "eligibility_disability",
    "eligibility_bpl",
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

print("Missing required columns:", missing_columns)

print("\n========== EMPTY SCHEME NAMES ==========")

empty_names = (
    df["name"]
    .fillna("")
    .astype(str)
    .str.strip()
    .eq("")
    .sum()
)

print("Empty names:", empty_names)

print("\n========== OFFICIAL URL CHECK ==========")

invalid_official = (
    df["official_url"].fillna("").astype(str).str.strip().ne("")
    &
    ~df["official_url"]
    .fillna("")
    .astype(str)
    .str.startswith(("http://", "https://"))
)

print("Invalid official URLs:", invalid_official.sum())

print("\n========== APPLY URL CHECK ==========")

invalid_apply = (
    df["apply_url_clean"].notna()
    &
    ~df["apply_url_clean"]
    .astype(str)
    .str.startswith(("http://", "https://"))
)

print("Invalid cleaned apply URLs:", invalid_apply.sum())

print("\n========== ELIGIBILITY CHECK ==========")

invalid_age = (
    df["eligibility_age_min"].notna()
    &
    df["eligibility_age_max"].notna()
    &
    (df["eligibility_age_min"] > df["eligibility_age_max"])
)

negative_age = (
    (df["eligibility_age_min"].notna() &
     (df["eligibility_age_min"] < 0))
    |
    (df["eligibility_age_max"].notna() &
     (df["eligibility_age_max"] < 0))
)

negative_income = (
    df["eligibility_income_max"].notna()
    &
    (df["eligibility_income_max"] < 0)
)

print("Invalid age ranges:", invalid_age.sum())
print("Negative ages:", negative_age.sum())
print("Negative income limits:", negative_income.sum())

print("\n========== GENDER ==========")

print(
    df["eligibility_gender"]
    .value_counts(dropna=False)
    .to_string()
)

print("\n========== RESIDENCE ==========")

print(
    df["eligibility_residence"]
    .value_counts(dropna=False)
    .to_string()
)

print("\n========== BOOLEAN FIELDS ==========")

print(
    "Disability:",
    df["eligibility_disability"]
    .value_counts(dropna=False)
    .to_dict()
)

print(
    "BPL:",
    df["eligibility_bpl"]
    .value_counts(dropna=False)
    .to_dict()
)

print("\n========== FINAL MISSING VALUES ==========")

print(
    df.isna()
    .sum()
    .sort_values(ascending=False)
    .to_string()
)

print("\n========== FINAL DATASET ==========")

print("Rows    :", len(df))
print("Columns :", len(df.columns))

print("\n========== AUDIT COMPLETE ==========")