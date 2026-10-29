import pandas as pd
import ast

INPUT_FILE = "data/processed/schemes_cleaned.csv"

df = pd.read_csv(INPUT_FILE)

print("\n========== ELIGIBILITY VALIDATION ==========")

# -------------------------------------------------
# 1. AGE VALIDATION
# -------------------------------------------------

invalid_age_range = df[
    (df["eligibility_age_min"].notna()) &
    (df["eligibility_age_max"].notna()) &
    (df["eligibility_age_min"] > df["eligibility_age_max"])
]

print("\n========== AGE RANGE ==========")
print("Invalid age ranges:", len(invalid_age_range))

if len(invalid_age_range) > 0:
    print(
        invalid_age_range[
            ["slug", "name", "eligibility_age_min", "eligibility_age_max"]
        ].to_string(index=False)
    )


# -------------------------------------------------
# 2. GENDER VALIDATION
# -------------------------------------------------

valid_genders = {"all", "male", "female"}

invalid_gender = df[
    ~df["eligibility_gender"].isin(valid_genders)
]

print("\n========== GENDER ==========")
print("Invalid gender values:", len(invalid_gender))


# -------------------------------------------------
# 3. RESIDENCE VALIDATION
# -------------------------------------------------

valid_residence = {"rural", "urban", "both"}

invalid_residence = df[
    ~df["eligibility_residence"].isin(valid_residence)
]

print("\n========== RESIDENCE ==========")
print("Invalid residence values:", len(invalid_residence))


# -------------------------------------------------
# 4. INCOME VALIDATION
# -------------------------------------------------

invalid_income = df[
    (df["eligibility_income_max"].notna()) &
    (df["eligibility_income_max"] < 0)
]

print("\n========== INCOME ==========")
print("Negative income limits:", len(invalid_income))


# -------------------------------------------------
# 5. AGE NEGATIVE VALUES
# -------------------------------------------------

negative_age = df[
    (
        (df["eligibility_age_min"].notna()) &
        (df["eligibility_age_min"] < 0)
    )
    |
    (
        (df["eligibility_age_max"].notna()) &
        (df["eligibility_age_max"] < 0)
    )
]

print("\n========== NEGATIVE AGE ==========")
print("Negative age values:", len(negative_age))


# -------------------------------------------------
# 6. BOOLEAN VALIDATION
# -------------------------------------------------

print("\n========== BOOLEAN FIELDS ==========")

print(
    "Disability values:",
    df["eligibility_disability"].value_counts(dropna=False).to_dict()
)

print(
    "BPL values:",
    df["eligibility_bpl"].value_counts(dropna=False).to_dict()
)


# -------------------------------------------------
# 7. ELIGIBILITY STATE FORMAT
# -------------------------------------------------

def check_state_format(value):
    try:
        parsed = ast.literal_eval(value)

        if isinstance(parsed, list):
            return True

        return False

    except:
        return False


invalid_state_format = df[
    ~df["eligibility_state"].apply(check_state_format)
]

print("\n========== ELIGIBILITY STATE ==========")
print("Invalid state formats:", len(invalid_state_format))

if len(invalid_state_format) > 0:
    print(
        invalid_state_format[
            ["slug", "name", "eligibility_state"]
        ].to_string(index=False)
    )


# -------------------------------------------------
# 8. CASTE FORMAT
# -------------------------------------------------

invalid_caste_format = df[
    ~df["eligibility_caste"].apply(check_state_format)
]

print("\n========== ELIGIBILITY CASTE ==========")
print("Invalid caste formats:", len(invalid_caste_format))


# -------------------------------------------------
# FINAL SUMMARY
# -------------------------------------------------

print("\n========== VALIDATION COMPLETE ==========")

print("Total records:", len(df))
print("Total columns:", len(df.columns))