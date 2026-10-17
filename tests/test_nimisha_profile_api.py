import unittest
from fastapi.testclient import TestClient
from backend.main import app
from Nimisha.services.profile_service import ProfileService


class TestNimishaProfileAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.service = ProfileService()

    def setUp(self):
        self.service.clear_all()

    def test_01_create_profile_success(self):
        payload = {
            "name": "Nimisha Mangal",
            "age": 21,
            "gender": "Female",
            "state": "Rajasthan",
            "district": "Jaipur",
            "income": 250000.0,
            "occupation": "Student",
            "category": "General",
            "disability_status": "No",
            "qualification": "B.Tech Data Science"
        }
        response = self.client.post("/api/profile", json=payload)
        self.assertEqual(response.status_code, 201)

        data = response.json()
        self.assertIn("profile_id", data)
        self.assertTrue(data["profile_id"].startswith("prof_"))
        self.assertEqual(data["name"], "Nimisha Mangal")
        self.assertEqual(data["age"], 21)
        self.assertEqual(data["state"], "Rajasthan")
        self.assertIn("created_at", data)
        self.assertIn("updated_at", data)

    def test_02_create_profile_validation_error_invalid_age(self):
        payload = {
            "name": "Invalid User",
            "age": -5,  # Invalid negative age
            "gender": "Male",
            "state": "Rajasthan",
            "district": "Jaipur",
            "income": 100000.0,
            "occupation": "Farmer",
            "category": "OBC"
        }
        response = self.client.post("/api/profile", json=payload)
        self.assertEqual(response.status_code, 422)

    def test_03_create_profile_validation_error_missing_field(self):
        payload = {
            "name": "Incomplete User",
            "age": 30
            # missing gender, state, district, income, occupation, category
        }
        response = self.client.post("/api/profile", json=payload)
        self.assertEqual(response.status_code, 422)

    def test_04_get_profile_success(self):
        payload = {
            "name": "Rohan Sharma",
            "age": 28,
            "gender": "Male",
            "state": "Delhi",
            "district": "North Delhi",
            "income": 180000.0,
            "occupation": "Artisan",
            "category": "OBC",
            "disability_status": "No"
        }
        create_res = self.client.post("/api/profile", json=payload)
        profile_id = create_res.json()["profile_id"]

        get_res = self.client.get(f"/api/profile/{profile_id}")
        self.assertEqual(get_res.status_code, 200)

        data = get_res.json()
        self.assertEqual(data["profile_id"], profile_id)
        self.assertEqual(data["name"], "Rohan Sharma")
        self.assertEqual(data["district"], "North Delhi")

    def test_05_get_profile_not_found(self):
        response = self.client.get("/api/profile/prof_nonexistent")
        self.assertEqual(response.status_code, 404)
        self.assertIn("not found", response.json()["detail"])

    def test_06_update_profile_success(self):
        payload = {
            "name": "Priya Verma",
            "age": 24,
            "gender": "Female",
            "state": "Madhya Pradesh",
            "district": "Bhopal",
            "income": 120000.0,
            "occupation": "Teacher",
            "category": "SC",
            "disability_status": "No"
        }
        create_res = self.client.post("/api/profile", json=payload)
        profile_id = create_res.json()["profile_id"]

        update_payload = {
            "income": 150000.0,
            "occupation": "Senior Teacher",
            "qualification": "M.Sc B.Ed"
        }
        update_res = self.client.put(f"/api/profile/{profile_id}", json=update_payload)
        self.assertEqual(update_res.status_code, 200)

        data = update_res.json()
        self.assertEqual(data["profile_id"], profile_id)
        self.assertEqual(data["income"], 150000.0)
        self.assertEqual(data["occupation"], "Senior Teacher")
        self.assertEqual(data["qualification"], "M.Sc B.Ed")
        self.assertEqual(data["name"], "Priya Verma")  # Unchanged field preserved

    def test_07_update_profile_not_found(self):
        update_payload = {"income": 300000.0}
        response = self.client.put("/api/profile/prof_nonexistent", json=update_payload)
        self.assertEqual(response.status_code, 404)
        self.assertIn("not found", response.json()["detail"])


if __name__ == "__main__":
    unittest.main()
