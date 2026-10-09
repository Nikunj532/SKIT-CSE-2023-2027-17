import pandas as pd

INPUT_FILE = "data/processed/schemes_cleaned_final.csv"

df = pd.read_csv(INPUT_FILE)

print("\n========== DUPLICATE NORMALIZED NAMES ==========")

name_counts = df["name"].value_counts()

duplicates = name_counts[name_counts > 1]

print("Duplicate names:", len(duplicates))

if len(duplicates) == 0:
    print("No duplicate scheme names found.")

else:
    for name in duplicates.index:
        print("\n" + "=" * 80)
        print("NAME:", name)
        print("=" * 80)

        matches = df[df["name"] == name]

        print(
            matches[
                [
                    "slug",
                    "name",
                    "state",
                    "category",
                    "official_url"
                ]
            ].to_string(index=False)
        )

print("\n========== COMPLETE ==========")