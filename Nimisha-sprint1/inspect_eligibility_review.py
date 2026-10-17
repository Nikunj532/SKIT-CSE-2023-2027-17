import pandas as pd

INPUT_FILE = "data/processed/eligibility_review.csv"

df = pd.read_csv(INPUT_FILE)

print("\n========== ELIGIBILITY REVIEW ==========")
print("Total records:", len(df))

for i, row in df.iterrows():

    print("\n" + "=" * 80)
    print(f"REVIEW #{i + 1}")
    print("=" * 80)

    print("Issue Type       :", row["issue_type"])
    print("Slug             :", row["slug"])
    print("Scheme Name      :", row["name"])
    print("Structured Value :", row["structured_value"])

    print("\nEligibility Text:")
    print(row["eligibility_text"])