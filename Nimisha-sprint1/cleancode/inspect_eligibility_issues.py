import pandas as pd
import re

INPUT_FILE = "data/processed/schemes_cleaned.csv"

df = pd.read_csv(INPUT_FILE)


def get_text(row):
    if pd.isna(row["eligibility_text"]):
        return ""
    return str(row["eligibility_text"]).lower()


# -------------------------------------------------
# FIND POSSIBLE ISSUES
# -------------------------------------------------

issues = []


for _, row in df.iterrows():

    text = get_text(row)
    slug = row["slug"]
    name = row["name"]

    # Gender
    gender = str(row["eligibility_gender"]).lower()

    if gender == "female":
        if not re.search(
            r"\bfemale\b|\bwomen\b|\bwoman\b|\bgirl\b|\bdaughter\b",
            text
        ):
            issues.append((slug, name, "gender", gender, text))

    elif gender == "male":
        if not re.search(
            r"\bmale\b|\bmen\b|\bman\b|\bboy\b|\bson\b",
            text
        ):
            issues.append((slug, name, "gender", gender, text))


    # BPL
    if row["eligibility_bpl"] is True:

        if not re.search(
            r"\bbpl\b|below poverty line|poverty line",
            text
        ):
            issues.append((slug, name, "bpl", True, text))


    # Disability
    if row["eligibility_disability"] is True:

        if not re.search(
            r"disabil|divyang|differently abled|special needs",
            text
        ):
            issues.append((slug, name, "disability", True, text))


    # Residence
    residence = str(row["eligibility_residence"]).lower()

    if residence == "rural":

        if not re.search(
            r"\brural\b|\bvillage\b|\bvillages\b",
            text
        ):
            issues.append((slug, name, "residence", residence, text))

    elif residence == "urban":

        if not re.search(
            r"\burban\b|\bcity\b|\bcities\b",
            text
        ):
            issues.append((slug, name, "residence", residence, text))


    # Age
    min_age = row["eligibility_age_min"]
    max_age = row["eligibility_age_max"]

    if pd.notna(min_age) or pd.notna(max_age):

        if not re.search(
            r"\bage\b|\byear old\b|\byears old\b|\byears\b",
            text
        ):
            issues.append((slug, name, "age", 
                           f"min={min_age}, max={max_age}", text))


    # Income
    income = row["eligibility_income_max"]

    if pd.notna(income):

        if not re.search(
            r"income|annual income|family income|household income",
            text
        ):
            issues.append((slug, name, "income", income, text))


# -------------------------------------------------
# DISPLAY
# -------------------------------------------------

print("\n========== POSSIBLE ISSUES ==========")
print("Total possible issues:", len(issues))


for i, issue in enumerate(issues, start=1):

    slug, name, issue_type, value, text = issue

    print("\n----------------------------------------")
    print(f"Issue #{i}")
    print(f"Type       : {issue_type}")
    print(f"Slug       : {slug}")
    print(f"Scheme     : {name}")
    print(f"Structured : {value}")
    print(f"Eligibility Text:\n{text[:1500]}")


print("\n========== INSPECTION COMPLETE ==========")