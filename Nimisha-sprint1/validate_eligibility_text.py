import pandas as pd
import re
import html

INPUT_FILE = "data/processed/schemes_cleaned.csv"
OUTPUT_FILE = "data/processed/eligibility_review.csv"

df = pd.read_csv(INPUT_FILE)

print("\n========== IMPROVED SEMANTIC ELIGIBILITY VALIDATION ==========")


# -------------------------------------------------
# 1. TEXT NORMALIZATION
# -------------------------------------------------

def normalize_text(value):
    if pd.isna(value):
        return ""

    text = str(value)

    # Decode HTML entities multiple times
    for _ in range(3):
        text = html.unescape(text)

    # Remove HTML tags
    text = re.sub(r"<[^>]+>", " ", text)

    # Normalize hyphens/dashes
    text = text.replace("–", "-")
    text = text.replace("—", "-")

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip().lower()


def get_combined_text(row):
    """
    Use both scheme name and eligibility text.
    """
    name = normalize_text(row["name"])
    eligibility = normalize_text(row["eligibility_text"])

    return f"{name} {eligibility}"


# -------------------------------------------------
# 2. PATTERN GROUPS
# -------------------------------------------------

FEMALE_PATTERNS = [
    r"\bfemale\b",
    r"\bwomen\b",
    r"\bwoman\b",
    r"\bgirl\b",
    r"\bgirls\b",
    r"\bdaughter\b",
    r"\bdaughters\b",
    r"\bwidow\b",
    r"\bwidows\b",
    r"\bvidhva\b",
    r"\bvridhva\b",
    r"\bpregnant\b",
    r"\bpregnancy\b",
    r"\bmaternity\b",
    r"\bmother\b",
    r"\bmothers\b",
    r"\bbride\b",
    r"\bwife\b",
    r"\bwives\b",
    r"\bfemale-headed\b",
    r"\bmahila\b",
    r"\bmahila mandal\b",
]

MALE_PATTERNS = [
    r"\bmale\b",
    r"\bmen\b",
    r"\bman\b",
    r"\bboy\b",
    r"\bboys\b",
    r"\bson\b",
    r"\bsons\b",
    r"\bfather\b",
    r"\bfathers\b",
    r"\bhusband\b",
    r"\bhusbands\b",
    r"\bwidower\b",
    r"\bbridegroom\b",
    r"\bpaternity\b",
]

DISABILITY_PATTERNS = [
    r"\bdisabil",
    r"\bdisabled\b",
    r"\bdifferently[- ]abled\b",
    r"\bdivyang\b",
    r"\bhandicapped\b",
    r"\bphysically challenged\b",
    r"\bphysically disabled\b",
    r"\bvisually impaired\b",
    r"\bvisually challenged\b",
    r"\bhearing impaired\b",
    r"\bhearing[- ]impaired\b",
    r"\bhearing challenged\b",
    r"\bspeech impaired\b",
    r"\bspeech challenged\b",
    r"\bblind\b",
    r"\bblindness\b",
    r"\blow vision\b",
    r"\bcerebral palsy\b",
    r"\bleprosy\b",
    r"\borthopedic",
    r"\borthopedically\b",
    r"\bmental retard",
    r"\bintellectual disabil",
    r"\bspecial needs\b",
    r"\blocomo",
    r"\bparalysis\b",
    r"\bparalytic\b",
    r"\bautism\b",
    r"\bmuscular dystrophy\b",
    r"\bhemophilia\b",
    r"\bthalassemia\b",
    r"\bsickle cell\b",
    r"\bdwarf\b",
    r"\bdwarfism\b",
    r"\bpermanent disablement\b",
    r"\bpartial permanent disablement\b",
    r"\bpermanently disabled\b",
    r"\bphysical or mental infirmity\b",
    r"\bphysically or mentally\b",
    r"\bloss of.*legs\b",
]

BPL_PATTERNS = [
    r"\bbpl\b",
    r"\bbelow poverty line\b",
    r"\bbelow-poverty-line\b",
    r"\bbelow poverty-line\b",
    r"\bpoverty line\b",
    r"\bpoverty-line\b",
    r"\bantyodaya\b",
    r"\baay\b",
]

RURAL_PATTERNS = [
    r"\brural\b",
    r"\bvillage\b",
    r"\bvillages\b",
    r"\bgram panchayat\b",
    r"\bgram panchayats\b",
]

URBAN_PATTERNS = [
    r"\burban\b",
    r"\bcity\b",
    r"\bcities\b",
    r"\btown\b",
    r"\btowns\b",
    r"\bmunicipality\b",
    r"\bmunicipal\b",
    r"\bmunicipal area\b",
    r"\bmunicipal areas\b",
    r"\bmunicipal corporation\b",
    r"\bmunicipal corporations\b",
]

AGE_PATTERNS = [
    r"\bage\b",
    r"\baged\b",
    r"\byear[- ]old\b",
    r"\byears?[- ]old\b",
    r"\byears?\s+of\s+age\b",
    r"\byears?\b",
    r"\byrs?\b",

    # Examples:
    # between 18 and 60
    # between the ages of 18 and 60
    r"\bbetween\b.{0,40}\b\d{1,3}\b.{0,15}\b\d{1,3}\b",

    # below 18 / under 18 / above 60
    r"\bbelow\s+\d{1,3}\b",
    r"\bunder\s+\d{1,3}\b",
    r"\babove\s+\d{1,3}\b",
    r"\bover\s+\d{1,3}\b",

    # at least 18 / not less than 18
    r"\bat least\s+\d{1,3}\b",
    r"\bnot less than\s+\d{1,3}\b",
    r"\bnot more than\s+\d{1,3}\b",

    # 18 and above / 60 or below
    r"\b\d{1,3}\s+(?:and|or)\s+(?:above|below)\b",

    # newborn / infant / adult
    r"\bnewborn\b",
    r"\bnewborns\b",
    r"\binfant\b",
    r"\binfants\b",
    r"\badult\b",
    r"\badults\b",
]

INCOME_PATTERNS = [
    r"\bincome\b",
    r"\bannual income\b",
    r"\bmonthly income\b",
    r"\bfamily income\b",
    r"\bhousehold income\b",
    r"\bannual family income\b",
    r"\bmonthly salary\b",
    r"\bsalary\b",
    r"\bwage\b",
    r"\bwages\b",
    r"\bearning\b",
    r"\bearnings\b",
    r"\bper annum\b",
    r"\bper month\b",
    r"\bfinancial income\b",
]


# -------------------------------------------------
# 3. MATCHING FUNCTION
# -------------------------------------------------

def contains_pattern(text, patterns):
    for pattern in patterns:
        if re.search(pattern, text):
            return True

    return False


# -------------------------------------------------
# 4. REVIEW LIST
# -------------------------------------------------

review_records = []


# -------------------------------------------------
# 5. GENDER VALIDATION
# -------------------------------------------------

for _, row in df.iterrows():

    gender = str(row["eligibility_gender"]).strip().lower()
    text = get_combined_text(row)

    if gender == "female":

        if not contains_pattern(text, FEMALE_PATTERNS):

            review_records.append({
                "slug": row["slug"],
                "name": row["name"],
                "issue_type": "gender_evidence_not_found",
                "structured_value": gender,
                "eligibility_text": row["eligibility_text"]
            })

    elif gender == "male":

        if not contains_pattern(text, MALE_PATTERNS):

            review_records.append({
                "slug": row["slug"],
                "name": row["name"],
                "issue_type": "gender_evidence_not_found",
                "structured_value": gender,
                "eligibility_text": row["eligibility_text"]
            })


# -------------------------------------------------
# 6. BPL VALIDATION
# -------------------------------------------------

for _, row in df.iterrows():

    if row["eligibility_bpl"] == True:

        text = get_combined_text(row)

        if not contains_pattern(text, BPL_PATTERNS):

            review_records.append({
                "slug": row["slug"],
                "name": row["name"],
                "issue_type": "bpl_evidence_not_found",
                "structured_value": True,
                "eligibility_text": row["eligibility_text"]
            })


# -------------------------------------------------
# 7. DISABILITY VALIDATION
# -------------------------------------------------

for _, row in df.iterrows():

    if row["eligibility_disability"] == True:

        text = get_combined_text(row)

        if not contains_pattern(text, DISABILITY_PATTERNS):

            review_records.append({
                "slug": row["slug"],
                "name": row["name"],
                "issue_type": "disability_evidence_not_found",
                "structured_value": True,
                "eligibility_text": row["eligibility_text"]
            })


# -------------------------------------------------
# 8. RESIDENCE VALIDATION
# -------------------------------------------------

for _, row in df.iterrows():

    residence = str(row["eligibility_residence"]).strip().lower()
    text = get_combined_text(row)

    if residence == "rural":

        if not contains_pattern(text, RURAL_PATTERNS):

            review_records.append({
                "slug": row["slug"],
                "name": row["name"],
                "issue_type": "rural_evidence_not_found",
                "structured_value": residence,
                "eligibility_text": row["eligibility_text"]
            })

    elif residence == "urban":

        if not contains_pattern(text, URBAN_PATTERNS):

            review_records.append({
                "slug": row["slug"],
                "name": row["name"],
                "issue_type": "urban_evidence_not_found",
                "structured_value": residence,
                "eligibility_text": row["eligibility_text"]
            })


# -------------------------------------------------
# 9. AGE VALIDATION
# -------------------------------------------------

for _, row in df.iterrows():

    min_age = row["eligibility_age_min"]
    max_age = row["eligibility_age_max"]

    if pd.notna(min_age) or pd.notna(max_age):

        text = get_combined_text(row)

        if not contains_pattern(text, AGE_PATTERNS):

            review_records.append({
                "slug": row["slug"],
                "name": row["name"],
                "issue_type": "age_evidence_not_found",
                "structured_value": f"{min_age} - {max_age}",
                "eligibility_text": row["eligibility_text"]
            })


# -------------------------------------------------
# 10. INCOME VALIDATION
# -------------------------------------------------

for _, row in df.iterrows():

    income = row["eligibility_income_max"]

    if pd.notna(income):

        text = get_combined_text(row)

        if not contains_pattern(text, INCOME_PATTERNS):

            review_records.append({
                "slug": row["slug"],
                "name": row["name"],
                "issue_type": "income_evidence_not_found",
                "structured_value": income,
                "eligibility_text": row["eligibility_text"]
            })


# -------------------------------------------------
# 11. SAVE REVIEW FILE
# -------------------------------------------------

review_df = pd.DataFrame(review_records)

if len(review_df) > 0:

    review_df.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8-sig"
    )


# -------------------------------------------------
# 12. FINAL SUMMARY
# -------------------------------------------------

print("\n========== VALIDATION SUMMARY ==========")

print("Total records:", len(df))
print("Records requiring review:", len(review_df))

if len(review_df) > 0:

    print("\nIssues by type:")

    print(
        review_df["issue_type"]
        .value_counts()
        .to_string()
    )

else:

    print("\nNo potential issues found.")

print("\nReview file:", OUTPUT_FILE)

print("\n========== COMPLETE ==========")