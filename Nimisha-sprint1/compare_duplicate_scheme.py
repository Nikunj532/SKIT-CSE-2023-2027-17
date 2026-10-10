import pandas as pd

INPUT_FILE = "data/processed/schemes_cleaned_final.csv"

df = pd.read_csv(INPUT_FILE)

slugs = [
    "free-ug-students-only",
    "freeship-ug-students-only"
]

columns = [
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
    "apply_url_clean",
    "official_url",
    "eligibility_age_min",
    "eligibility_age_max",
    "eligibility_gender",
    "eligibility_caste",
    "eligibility_income_max",
    "eligibility_residence",
    "eligibility_state",
    "eligibility_disability",
    "eligibility_bpl"
]

matches = df[df["slug"].isin(slugs)][columns]

for _, row in matches.iterrows():
    print("\n" + "=" * 100)
    print("SLUG:", row["slug"])
    print("=" * 100)

    for col in columns:
        print(f"\n--- {col} ---")
        print(row[col])

print("\n" + "=" * 100)
print("COMPARISON COMPLETE")
print("=" * 100)