import logging
import re
from typing import List, Optional, Tuple

from backend.schemas.scheme import Scheme
from backend.services.scheme_service import get_all_schemes, get_scheme_by_id
from Nimisha.schemas.profile import ProfileBase, ProfileResponse
from Nimisha.schemas.recommendation import (
    EligibilityCheckResult,
    EligibilityStatus,
    RecommendationResponse,
    SchemeEligibilityMatch,
)
from Nimisha.services.profile_service import ProfileService

logger = logging.getLogger("adhikar_setu.recommendation_service")


class RecommendationService:
    """
    Personalized Scheme Recommendation & Eligibility Engine.
    Evaluates citizen demographics, income, social category, and location
    against government scheme requirements to produce ranked, explainable recommendations.
    """

    def __init__(self, profile_service: Optional[ProfileService] = None):
        self.profile_service = profile_service or ProfileService()

    @staticmethod
    def _extract_income_ceiling(scheme: Scheme, citizen_category: str) -> Optional[float]:
        """
        Parses income ceilings from scheme eligibility text and specific known rules.
        """
        full_text = " ".join(scheme.eligibility + [scheme.description, scheme.name]).lower()

        # Specific known state/central scheme thresholds
        if scheme.scheme_id == "sch_devnarayan_sc" or "devnarayan" in full_text:
            return 250000.0

        if scheme.scheme_id == "sch_post_matric_scholarship" or "post-matric" in full_text:
            cat_upper = citizen_category.upper()
            if "OBC" in cat_upper:
                return 150000.0
            return 250000.0

        # Regex search for Rs. X Lakhs or ceiling patterns
        # Matches e.g. "2.5 lakhs", "2,50,000", "1.5 lakh"
        lakh_match = re.search(r'(?:rs\.?|inr)?\s*([0-9]+(?:\.[0-9]+)?)\s*(?:lakh|lakhs)', full_text)
        if lakh_match:
            try:
                lakhs = float(lakh_match.group(1))
                return lakhs * 100000.0
            except ValueError:
                pass

        num_match = re.search(r'(?:rs\.?|inr)\s*([0-9]{1,2}(?:,[0-9]{2,3})+)', full_text)
        if num_match:
            try:
                num_str = num_match.group(1).replace(",", "")
                return float(num_str)
            except ValueError:
                pass

        return None

    def evaluate_scheme_eligibility(
        self,
        profile: ProfileBase,
        scheme: Scheme
    ) -> SchemeEligibilityMatch:
        """
        Evaluates a single scheme against a citizen profile and produces
        structured eligibility determination with explainable criteria breakdown.
        """
        score = 0.0
        matched: List[str] = []
        missing: List[str] = []
        hard_disqualified = False

        scheme_text = (
            f"{scheme.name} {scheme.description} {scheme.category} "
            f"{' '.join(scheme.eligibility)} {' '.join(scheme.benefits)}"
        ).lower()

        # -------------------------------------------------------------
        # 1. Geographic Alignment (Weight: 25 points)
        # -------------------------------------------------------------
        scheme_state = (scheme.state or "Central").strip()
        scheme_state_lower = scheme_state.lower()
        citizen_state_lower = profile.state.strip().lower()

        is_national = scheme_state_lower in ("central", "all", "all india", "national")
        if is_national:
            score += 25.0
            matched.append(f"Scheme is centrally sponsored and accessible across all states including {profile.state}")
        elif scheme_state_lower == citizen_state_lower:
            score += 25.0
            matched.append(f"Resident of {profile.state} matches scheme jurisdiction")
        else:
            missing.append(f"Scheme is restricted to {scheme_state}; citizen resides in {profile.state}")
            hard_disqualified = True

        # -------------------------------------------------------------
        # 2. Income Constraint Evaluation (Weight: 25 points)
        # -------------------------------------------------------------
        income_ceiling = self._extract_income_ceiling(scheme, profile.category)
        if income_ceiling is not None:
            if profile.income <= income_ceiling:
                score += 25.0
                matched.append(
                    f"Annual income ₹{profile.income:,.0f} satisfies scheme income ceiling of ₹{income_ceiling:,.0f}"
                )
            else:
                missing.append(
                    f"Annual income ₹{profile.income:,.0f} exceeds maximum ceiling of ₹{income_ceiling:,.0f}"
                )
                hard_disqualified = True
        else:
            # Scheme has no explicit upper ceiling cap
            if profile.income <= 500000.0:
                score += 25.0
                matched.append("Income profile qualifies under standard public welfare criteria")
            else:
                score += 15.0
                matched.append("Scheme has universal or broad eligibility criteria without strict income ceiling")

        # -------------------------------------------------------------
        # 3. Target Domain & Occupation Alignment (Weight: 30 points)
        # -------------------------------------------------------------
        occ_lower = profile.occupation.strip().lower()
        cat_lower = scheme.category.strip().lower()

        if occ_lower in ("student", "learner"):
            if "education" in cat_lower or any(w in scheme_text for w in ("scholarship", "study", "student", "gurukul", "school")):
                score += 30.0
                matched.append("Citizen occupation 'Student' strongly aligns with education and academic welfare objectives")
            else:
                score += 12.0
                matched.append("Broad welfare scheme applicable to student household")
        elif occ_lower in ("farmer", "cultivator", "agriculture", "kisan"):
            if "agriculture" in cat_lower or any(w in scheme_text for w in ("farmer", "kisan", "cultivable", "landholding")):
                score += 30.0
                matched.append("Occupation 'Farmer' qualifies for agricultural subsidy and direct income support")
            else:
                score += 15.0
                matched.append("Broad household scheme accessible to farmer families")
        elif occ_lower in ("artisan", "craftsman", "weaver"):
            if any(w in scheme_text for w in ("artisan", "vishwakarma", "handicraft", "skill")):
                score += 30.0
                matched.append("Occupation qualifies for artisanal and skill-development schemes")
            else:
                score += 15.0
        elif occ_lower in ("worker", "labour", "daily wage", "contractual"):
            if any(w in scheme_text for w in ("worker", "labour", "shramik", "unorganised", "contractual")):
                score += 30.0
                matched.append("Worker employment category qualifies for labor and social security benefits")
            else:
                score += 15.0
        else:
            # Broad citizen occupations
            if cat_lower in ("health", "housing", "social welfare"):
                score += 25.0
                matched.append(f"Scheme category '{scheme.category}' serves universal citizen households regardless of trade")
            else:
                score += 15.0

        # If agricultural scheme requires landholding and citizen is student/unrelated
        if ("landholding" in scheme_text or "kisan" in scheme_text) and occ_lower not in ("farmer", "agriculture"):
            missing.append("Requires cultivable agricultural landholding ownership (e.g. Khatauni)")

        # -------------------------------------------------------------
        # 4. Social Category & Reserved Groups (Weight: 20 points)
        # -------------------------------------------------------------
        citizen_cat_upper = profile.category.strip().upper()
        scheme_mentions_sc_st = any(tag in scheme_text for tag in ("sc/st", "sc ", "st ", "scheduled caste", "scheduled tribe"))
        scheme_mentions_obc = "obc" in scheme_text or "backward" in scheme_text

        if scheme.scheme_id == "sch_devnarayan_sc":
            # Designated for Special Backward Classes (Gujjar, Raika, etc.)
            if citizen_cat_upper in ("OBC", "SBC", "SC", "ST"):
                score += 20.0
                matched.append(f"Social category '{profile.category}' meets backward classes priority criteria")
            else:
                missing.append("Designated primarily for Special Backward Classes (e.g. Gujjar, Raika, Gadaria)")
                score += 5.0
        elif scheme.scheme_id == "sch_post_matric_scholarship":
            if citizen_cat_upper in ("SC", "ST", "OBC"):
                score += 20.0
                matched.append(f"Citizen social category '{profile.category}' meets scholarship reservation criteria")
            else:
                missing.append("Restricted to SC, ST, and OBC category students")
                hard_disqualified = True
        elif scheme_mentions_sc_st or scheme_mentions_obc:
            if citizen_cat_upper in ("SC", "ST", "OBC", "EWS"):
                score += 20.0
                matched.append(f"Category '{profile.category}' qualifies under designated affirmative action criteria")
            else:
                score += 10.0
                matched.append("General category applicant eligible under standard open provisions")
        else:
            # Universal social category
            score += 20.0
            matched.append("Scheme open to citizens across all social categories")

        # -------------------------------------------------------------
        # 5. Disability & Special Inclusions
        # -------------------------------------------------------------
        if profile.disability_status and profile.disability_status.strip().lower() in ("yes", "true", "1"):
            if "disability" in scheme_text or "divyang" in scheme_text:
                score += 10.0
                matched.append("Disability status qualifies citizen for targeted assistance")

        # Cap score between 0.0 and 100.0
        final_score = min(100.0, max(0.0, round(score, 1)))

        # Determine eligibility status
        if hard_disqualified or final_score < 40.0:
            is_eligible = False
            status = EligibilityStatus.INELIGIBLE
            reason = (
                f"Currently ineligible due to criteria restrictions "
                f"({missing[0] if missing else 'criteria not met'})."
            )
        elif final_score >= 70.0 and len(missing) == 0:
            is_eligible = True
            status = EligibilityStatus.ELIGIBLE
            reason = (
                f"Highly recommended: {profile.name} satisfies state residency, income threshold, "
                f"and {profile.occupation.lower()} profile requirements."
            )
        else:
            is_eligible = True
            status = EligibilityStatus.CONDITIONALLY_ELIGIBLE
            reason = (
                f"Conditionally eligible (score {final_score:.0f}%): requires documentation verification "
                f"({missing[0] if missing else 'subject to document review'})."
            )

        return SchemeEligibilityMatch(
            scheme_id=scheme.scheme_id,
            name=scheme.name,
            category=scheme.category,
            state=scheme.state,
            ministry=scheme.ministry,
            official_url=scheme.official_url,
            is_eligible=is_eligible,
            match_score=final_score,
            eligibility_status=status,
            matched_criteria=matched,
            missing_criteria=missing,
            recommendation_reason=reason,
            benefits_summary=scheme.benefits,
        )

    def recommend_for_profile(
        self,
        profile: ProfileBase,
        min_score: float = 40.0,
        category: Optional[str] = None,
        limit: int = 10,
        profile_id: Optional[str] = None,
    ) -> RecommendationResponse:
        """
        Evaluates all available schemes against a given citizen profile
        and returns personalized, ranked recommendations.
        """
        all_schemes = get_all_schemes()
        evaluated_matches: List[SchemeEligibilityMatch] = []

        for scheme in all_schemes:
            if category and category.strip():
                if category.strip().lower() not in scheme.category.lower():
                    continue

            match = self.evaluate_scheme_eligibility(profile, scheme)
            if match.is_eligible and match.match_score >= min_score:
                evaluated_matches.append(match)

        # Sort by match score descending, then by name
        evaluated_matches.sort(key=lambda m: (-m.match_score, m.name))

        paged_recommendations = evaluated_matches[:limit]

        return RecommendationResponse(
            profile_id=profile_id,
            citizen_name=profile.name,
            state=profile.state,
            category=profile.category,
            occupation=profile.occupation,
            total_recommended=len(evaluated_matches),
            total_evaluated=len(all_schemes),
            recommendations=paged_recommendations,
        )

    def recommend_by_profile_id(
        self,
        profile_id: str,
        min_score: float = 40.0,
        category: Optional[str] = None,
        limit: int = 10,
    ) -> Optional[RecommendationResponse]:
        """
        Fetches an existing profile by ID and returns personalized scheme recommendations.
        """
        profile = self.profile_service.get_profile(profile_id)
        if not profile:
            return None

        # Convert ProfileResponse to ProfileBase for evaluation
        profile_base = ProfileBase(
            name=profile.name,
            age=profile.age,
            gender=profile.gender,
            state=profile.state,
            district=profile.district,
            income=profile.income,
            occupation=profile.occupation,
            category=profile.category,
            disability_status=profile.disability_status,
            qualification=profile.qualification,
        )

        return self.recommend_for_profile(
            profile=profile_base,
            min_score=min_score,
            category=category,
            limit=limit,
            profile_id=profile_id,
        )

    def check_scheme_eligibility(
        self,
        profile: ProfileBase,
        scheme_id: str,
    ) -> Optional[EligibilityCheckResult]:
        """
        Evaluates eligibility for one specific scheme against a citizen profile.
        """
        scheme = get_scheme_by_id(scheme_id)
        if not scheme:
            return None

        match = self.evaluate_scheme_eligibility(profile, scheme)
        return EligibilityCheckResult(
            scheme_id=match.scheme_id,
            scheme_name=match.name,
            is_eligible=match.is_eligible,
            eligibility_status=match.eligibility_status,
            match_score=match.match_score,
            matched_criteria=match.matched_criteria,
            missing_criteria=match.missing_criteria,
            recommendation_reason=match.recommendation_reason,
        )
