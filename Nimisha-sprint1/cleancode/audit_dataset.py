import pandas as pd

FILE_PATH = "data/raw/Schemes.csv"

df = pd.read_csv(FILE_PATH)

print("\n========== DATASET SHAPE ==========")
print(f"Rows    : {df.shape[0]}")
print(f"Columns : {df.shape[1]}")

print("\n========== COLUMNS ==========")
for i, column in enumerate(df.columns, start=1):
    print(f"{i}. {column}")

print("\n========== DATA TYPES ==========")
print(df.dtypes)

print("\n========== MISSING VALUES ==========")
missing = df.isnull().sum()
missing_percentage = (missing / len(df) * 100).round(2)

missing_report = pd.DataFrame({
    "missing_count": missing,
    "missing_percentage": missing_percentage
})

print(missing_report.sort_values(
    "missing_percentage",
    ascending=False
))

print("\n========== DUPLICATE ROWS ==========")
print("Duplicate rows:", df.duplicated().sum())

print("\n========== DUPLICATE SLUGS ==========")
print("Duplicate slugs:", df["slug"].duplicated().sum())

print("\n========== DUPLICATE NAMES ==========")
print("Duplicate names:", df["name"].duplicated().sum())

print("\n========== UNIQUE STATES ==========")
print(df["state"].value_counts(dropna=False))

print("\n========== UNIQUE GENDERS ==========")
print(df["eligibility_gender"].value_counts(dropna=False))

print("\n========== UNIQUE RESIDENCE ==========")
print(df["eligibility_residence"].value_counts(dropna=False))

print("\n========== SAMPLE RECORD ==========")
print(df.iloc[0].to_string())