import unittest
from fastapi.testclient import TestClient
from backend.main import app
from Nimisha.services.profile_service import ProfileService
from Nimisha.services.recommendation_service import RecommendationService
from Nimisha.schemas.profile import ProfileBase, ProfileCreate
from Nimisha.schemas.recommendation import EligibilityStatus


class TestNimishaRecommendationAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.profile_service = ProfileService()
        cls.rec_service = RecommendationService(profile_service=cls.profile_service)

    def setUp(self):
        self.profile_service.clear_all()

    def test_01_recommendations_for_student_profile(self):
        """Student in Rajasthan with low income should get Education and healthcare schemes."""
        profile_res = self.client.post("/api/profile", json={
            "name": "Nimisha Mangal",
            "age": 21,
            "gender": "Female",
            "state": "Rajasthan",
            "district": "Jaipur",
            "income": 120000.0,
            "occupation": "Student",
            "category": "OBC",
            "disability_status": "No",
            "qualification": "B.Tech Data Science"
        })
        self.assertEqual(profile_res.status_code, 201)
        profile_id = profile_res.json()["profile_id"]

        rec_res = self.client.get(f"/api/profile/{profile_id}/recommendations")
        self.assertEqual(rec_res.status_code, 200)

        data = rec_res.json()
        self.assertEqual(data["profile_id"], profile_id)
        self.assertEqual(data["citizen_name"], "Nimisha Mangal")
        self.assertGreater(data["total_recommended"], 0)
        self.assertGreater(len(data["recommendations"]), 0)

        # Check top recommended scheme
        top_rec = data["recommendations"][0]
        self.assertIn("scheme_id", top_rec)
        self.assertIn("match_score", top_rec)
        self.assertGreaterEqual(top_rec["match_score"], 40.0)
        self.assertIn(top_rec["eligibility_status"], ("Eligible", "Conditionally Eligible"))
        self.assertIsInstance(top_rec["matched_criteria"], list)
        self.assertGreater(len(top_rec["matched_criteria"]), 0)
        self.assertTrue(len(top_rec["recommendation_reason"]) > 0)

        # Confirm Post-Matric Scholarship is among recommended schemes for OBC student
        scheme_ids = [r["scheme_id"] for r in data["recommendations"]]
        self.assertIn("sch_post_matric_scholarship", scheme_ids)

    def test_02_recommendations_for_farmer_profile(self):
        """Farmer in UP/Central should qualify strongly for PM-KISAN."""
        profile_res = self.client.post("/api/profile", json={
            "name": "Ramesh Patel",
            "age": 42,
            "gender": "Male",
            "state": "Uttar Pradesh",
            "district": "Varanasi",
            "income": 95000.0,
            "occupation": "Farmer",
            "category": "OBC",
            "disability_status": "No"
        })
        self.assertEqual(profile_res.status_code, 201)
        profile_id = profile_res.json()["profile_id"]

        rec_res = self.client.get(f"/api/profile/{profile_id}/recommendations")
        self.assertEqual(rec_res.status_code, 200)

        data = rec_res.json()
        rec_ids = [r["scheme_id"] for r in data["recommendations"]]
        self.assertIn("sch_pm_kisan", rec_ids)

        pm_kisan_match = next(r for r in data["recommendations"] if r["scheme_id"] == "sch_pm_kisan")
        self.assertEqual(pm_kisan_match["eligibility_status"], "Eligible")
        self.assertGreaterEqual(pm_kisan_match["match_score"], 80.0)

        # UP resident should NOT be eligible for Rajasthan-only schemes
        self.assertNotIn("sch_mukhyamantri_chiranjeevi", rec_ids)

    def test_03_recommendations_ad_hoc_post_endpoint(self):
        """POST /api/recommendations enables guest citizens to discover eligible schemes."""
        payload = {
            "name": "Ananya Sharma",
            "age": 22,
            "gender": "Female",
            "state": "Rajasthan",
            "district": "Udaipur",
            "income": 180000.0,
            "occupation": "Student",
            "category": "General",
            "disability_status": "No"
        }
        res = self.client.post("/api/recommendations", json=payload)
        self.assertEqual(res.status_code, 200)

        data = res.json()
        self.assertIsNone(data["profile_id"])
        self.assertEqual(data["citizen_name"], "Ananya Sharma")
        self.assertGreater(data["total_recommended"], 0)

    def test_04_recommendations_category_and_score_filters(self):
        """Filter recommendations by category and minimum score."""
        payload = {
            "name": "Kavita Rao",
            "age": 20,
            "gender": "Female",
            "state": "Rajasthan",
            "district": "Jaipur",
            "income": 100000.0,
            "occupation": "Student",
            "category": "SC",
            "disability_status": "No"
        }
        # Filter by Education category
        res = self.client.post("/api/recommendations?category=Education&min_score=70", json=payload)
        self.assertEqual(res.status_code, 200)

        data = res.json()
        for rec in data["recommendations"]:
            self.assertEqual(rec["category"], "Education")
            self.assertGreaterEqual(rec["match_score"], 70.0)

    def test_05_check_scheme_eligibility_endpoint_success(self):
        """POST /api/schemes/{scheme_id}/check-eligibility gives in-depth audit."""
        payload = {
            "name": "Priya Singh",
            "age": 21,
            "gender": "Female",
            "state": "Rajasthan",
            "district": "Jaipur",
            "income": 120000.0,
            "occupation": "Student",
            "category": "SC",
            "disability_status": "No"
        }
        res = self.client.post(
            "/api/schemes/sch_post_matric_scholarship/check-eligibility",
            json=payload
        )
        self.assertEqual(res.status_code, 200)

        data = res.json()
        self.assertEqual(data["scheme_id"], "sch_post_matric_scholarship")
        self.assertTrue(data["is_eligible"])
        self.assertEqual(data["eligibility_status"], "Eligible")
        self.assertGreaterEqual(data["match_score"], 80.0)
        self.assertGreater(len(data["matched_criteria"]), 0)

    def test_06_check_scheme_eligibility_disqualified_income(self):
        """Citizen exceeding income ceiling is marked ineligible."""
        payload = {
            "name": "High Income Student",
            "age": 21,
            "gender": "Male",
            "state": "Rajasthan",
            "district": "Jaipur",
            "income": 600000.0,  # Exceeds Rs. 2.5L / 1.5L ceiling
            "occupation": "Student",
            "category": "OBC",
            "disability_status": "No"
        }
        res = self.client.post(
            "/api/schemes/sch_post_matric_scholarship/check-eligibility",
            json=payload
        )
        self.assertEqual(res.status_code, 200)

        data = res.json()
        self.assertFalse(data["is_eligible"])
        self.assertEqual(data["eligibility_status"], "Ineligible")
        self.assertTrue(any("exceeds" in m.lower() for m in data["missing_criteria"]))

    def test_07_recommendations_not_found_profile(self):
        """GET /api/profile/prof_unknown/recommendations returns 404."""
        res = self.client.get("/api/profile/prof_unknown_999/recommendations")
        self.assertEqual(res.status_code, 404)
        self.assertIn("not found", res.json()["detail"])

    def test_08_check_scheme_not_found(self):
        """POST /api/schemes/sch_unknown/check-eligibility returns 404."""
        payload = {
            "name": "Test User",
            "age": 25,
            "gender": "Male",
            "state": "Rajasthan",
            "district": "Jaipur",
            "income": 200000.0,
            "occupation": "Worker",
            "category": "General",
            "disability_status": "No"
        }
        res = self.client.post("/api/schemes/sch_nonexistent_xyz/check-eligibility", json=payload)
        self.assertEqual(res.status_code, 404)


if __name__ == "__main__":
    unittest.main()
