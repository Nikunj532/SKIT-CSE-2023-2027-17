import pandas as pd

INPUT_FILE = "data/processed/schemes_cleaned_final.csv"
OUTPUT_FILE = "data/processed/schemes_cleaned_final.csv"

REMOVE_SLUG = "freeship-ug-students-only"

df = pd.read_csv(INPUT_FILE)

before = len(df)

df = df[df["slug"] != REMOVE_SLUG].copy()

after = len(df)

print("Rows before:", before)
print("Rows after:", after)
print("Removed:", before - after)

df.to_csv(OUTPUT_FILE, index=False)

print("\nDuplicate scheme removed successfully.")